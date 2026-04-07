# Development Guide

Local development setup, testing patterns, and contribution guidelines for the OpenEnv Business Growth environment.

---

## Local Setup

### Prerequisites

- Python 3.9+
- pip or conda
- Git

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd opencv_pro-main

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### Optional: Development Tools

For testing and code quality:

```bash
pip install pytest pytest-cov black mypy flake8
```

---

## Project Structure

```
env/
├── business_env.py              # Main OpenEnv interface
├── models/
│   ├── schemas.py               # Pydantic data classes
│   └── __init__.py
├── tasks/
│   ├── base_task.py             # Abstract task class
│   ├── task1_social_media.py    # Easy: Social Media
│   ├── task2_review_management.py  # Medium: Reviews
│   └── task3_revenue_optimization.py  # Hard: Revenue
└── graders/
    ├── base_grader.py
    ├── grader1.py
    ├── grader2.py
    └── grader3.py

agent/
├── action_parser.py             # LLM text → Action
├── openai_client.py             # OpenAI factory
├── baseline_agent.py            # Heuristic agent
└── capabilities/                # Optional (not in Docker)
```

---

## Running Tests

### All Tests

```bash
pytest tests -v
```

### Contract Compliance Tests

```bash
# Validates output format, determinism, etc.
python tests/test_inference_contract.py
```

### Specific Test

```bash
pytest tests/test_agent.py -v -k "test_name"
```

### Coverage Report

```bash
pytest tests --cov=env --cov=agent --cov-report=html
# View: htmlcov/index.html
```

---

## Adding a New Task

### 1. Create Task Class

**File: `env/tasks/task4_new_task.py`**

```python
from __future__ import annotations
from typing import Any, Dict, List, Tuple
from env.tasks.base_task import BaseTask
from env.models.schemas import ActionType

class NewTask(BaseTask):
    TASK_ID = 4
    DESCRIPTION = "New Task Description"
    MAX_STEPS = 10
    
    def initial_state(self, rng: Any) -> Dict[str, Any]:
        """Return initial state dict."""
        return {
            "metric_a": 100,
            "metric_b": 0.5,
            "step": 0,
        }
    
    def apply_action(
        self,
        state: Dict[str, Any],
        action_type: str,
        parameters: Dict[str, Any],
        rng: Any,
        action_history: List[str],
    ) -> Tuple[Dict[str, Any], bool]:
        """Apply action and return (new_state, goal_reached)."""
        new_state = state.copy()
        goal_reached = False
        
        if action_type == "action_name":
            new_state["metric_a"] += parameters.get("amount", 10)
        
        goal_reached = new_state["metric_a"] >= 500
        return new_state, goal_reached
    
    def get_valid_actions(self) -> List[str]:
        """Return valid action types."""
        return ["action_name", "other_action", "no_op"]
```

### 2. Register in BusinessEnv

**File: `env/business_env.py`** (modify `_TASKS` dict):

```python
from env.tasks.task4_new_task import NewTask

_TASKS: Dict[int, type] = {
    1: SocialMediaTask,
    2: ReviewManagementTask,
    3: RevenueOptimizationTask,
    4: NewTask,  # Add new task
}
```

### 3. Add Grader

**File: `env/graders/grader4.py`**

```python
from env.graders.base_grader import BaseGrader

class Grader4(BaseGrader):
    TASK_ID = 4
    
    def grade(self, state: Dict[str, Any]) -> float:
        """Return score in [0.0, 1.0]."""
        metric_a = state.get("metric_a", 0)
        return min(1.0, metric_a / 500.0)
```

### 4. Test

```bash
python -c "
from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType

env = BusinessEnv(task_id=4, seed=42)
obs = env.reset()
print(f'Initial observation: {obs}')

action = Action(action_type=ActionType.NO_OP)
result = env.step(action)
print(f'Reward: {result.reward.value}')
"
```

---

## Extending Action Space

### Add Action Type

**File: `env/models/schemas.py`**

```python
class ActionType(str, Enum):
    # ... existing actions ...
    NEW_ACTION = "new_action"
```

### Update Task

```python
def apply_action(self, state, action_type, parameters, rng, action_history):
    if action_type == "new_action":
        # Handle implementation
        pass
```

### Update LLM Prompts

**File: `agent/action_parser.py`**

```python
TASK_ACTION_PROMPTS: Dict[int, str] = {
    1: (
        # ... existing prompt ...
        "  new_action       — param1: type, param2: type\n"
        # ... rest of prompt ...
    )
}
```

---

## Code Quality

### Type Checking

```bash
mypy env agent --ignore-missing-imports
```

### Linting

```bash
flake8 env agent --max-line-length=100
```

### Formatting

```bash
black env agent tests --line-length=100
```

### Pre-commit Hook (Optional)

```bash
# Create .git/hooks/pre-commit
#!/bin/bash
black --check env agent tests
flake8 env agent tests
pytest tests -q
```

---

## Debugging

### Enable Logging

```bash
export LOG_LEVEL=DEBUG
python inference.py
```

### Interactive Debugging

```python
import pdb
pdb.set_trace()  # Breakpoint

# Or use IPython
from IPython import embed
embed()  # IPython shell
```

### Environment Variables

```bash
# Override defaults
export SEED=123
export USE_LLM=false
export API_BASE_URL=https://api.openai.com/v1
export MODEL_NAME=gpt-4o-mini

python inference.py
```

---

## Common Tasks

### Run Interactive CLI

```bash
python main.py
```

### Run Agent Baseline

```bash
python agent/baseline_agent.py
```

### Run Single Task

```python
from env.business_env import BusinessEnv
from env.models.schemas import Action, ActionType

env = BusinessEnv(task_id=1, seed=42)
obs = env.reset()

for step in range(10):
    obs = env.reset()
    print(f"Step {step}: Observation = {obs}")
    
    action = Action(action_type=ActionType.NO_OP)
    result = env.step(action)
    print(f"Reward: {result.reward.value}")
    
    if result.done:
        break
```

### Validate Determinism

```bash
# Run twice, should see identical action sequences
python inference.py > run1.txt
python inference.py > run2.txt
diff run1.txt run2.txt
```

---

## Troubleshooting

### Module Import Error

```
ModuleNotFoundError: No module named 'env'
```

**Fix:** Ensure Python path includes repository root:
```bash
export PYTHONPATH=$PWD:$PYTHONPATH
python inference.py
```

### Pydantic Validation Error

```
ValidationError: 1 validation error for Action
```

**Fix:** Check action format matches schema in `env/models/schemas.py`

### OpenAI Client Error

```
AuthenticationError: Invalid API key provided
```

**Fix:** Verify OPENAI_API_KEY environment variable is set:
```bash
echo $OPENAI_API_KEY
```

---

## Performance Profiling

### Using cProfile

```python
import cProfile
import pstats
import inference

cProfile.run('inference.main()', 'profile.stats')
stats = pstats.Stats('profile.stats')
stats.sort_stats('cumsum').print_stats(10)
```

### Memory Usage

```bash
pip install memory-profiler

python -m memory_profiler inference.py
```

---

## Version Control

### Commit Guidelines

```bash
# Good commit messages
git commit -m "Fix: Ensure [END] emitted on exceptions"
git commit -m "Feature: Add task 4 revenue optimization"
git commit -m "Docs: Improve README with examples"

# Avoid
git commit -m "fixes"
git commit -m "WIP"
```

### Branch Strategy

```bash
# Feature branch
git checkout -b feature/new-task-4
# ... make changes ...
git push origin feature/new-task-4

# Then create pull request on GitHub
```

---

## Documentation

### Docstring Format

```python
def my_function(param1: str, param2: int) -> bool:
    """Short description.
    
    Longer description if needed.
    
    Parameters
    ----------
    param1 : str
        Description of param1.
    param2 : int
        Description of param2.
        
    Returns
    -------
    bool
        Description of return value.
    """
    return True
```

---

## Resources

- **OpenEnv Spec**: See README.md
- **Pydantic Docs**: https://docs.pydantic.dev/
- **OpenAI API**: https://platform.openai.com/docs/api-reference
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

---

**Need help?** Check existing tests or create an issue!
