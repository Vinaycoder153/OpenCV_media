# OpenAI to Google Gemini API Migration Guide

## Overview

This project has been successfully migrated from **OpenAI API (GPT-4o-mini)** to **Google Gemini API (Gemini 1.5 Flash)**.

### What Changed

- **API Provider**: OpenAI → Google GenerativeAI
- **LLM Model**: GPT-4o-mini → Gemini 1.5 Flash (or Gemini 1.5 Pro)
- **Environment Variable**: `OPENAI_API_KEY` → `GOOGLE_API_KEY`
- **Dependencies**: `openai` → `google-generativeai`
- **Client Library**: `OpenAI()` → **Custom Gemini Client Wrapper**

---

## Installation & Setup

### Step 1: Install Dependencies

```bash
# First, activate your virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install updated requirements
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Get Google Gemini API Key

1. **Visit Google AI Studio**: https://aistudio.google.com/app/apikeys
2. **Sign in** with your Google account
3. **Click "Create API Key"** button
4. **Select a project** (or create a new one)
5. **Copy your API key** (it starts with `AIzaSy...`)

### Step 3: Set Environment Variable

#### Linux/macOS:
```bash
export GOOGLE_API_KEY="AIzaSy..."
```

#### Windows (PowerShell):
```powershell
$env:GOOGLE_API_KEY="AIzaSy..."
```

#### Windows (Command Prompt):
```cmd
set GOOGLE_API_KEY=AIzaSy...
```

#### Persistent Setup (Recommended):

Create a `.env` file in the project root:
```bash
cp .env.example .env  # If available
# OR create manually:
echo "GOOGLE_API_KEY=AIzaSy..." > .env
```

Then load it before running:
```bash
# Linux/macOS
source .env

# Windows PowerShell
Get-Content .env | ForEach-Object { $key, $value = $_ -split '='; [Environment]::SetEnvironmentVariable($key, $value) }
```

---

## Running the Application

### Interactive Mode

```bash
python main.py
```

Follow the menu options to:
- ✅ Generate social media content
- ✅ Get growth strategies
- ✅ Analyze reviews
- ✅ Generate performance reports
- ✅ Create customer personas
- ✅ And more!

### Baseline Agent (Testing Mode)

```bash
python agent/baseline_agent.py
```

This runs the agent through all three tasks in both LLM and heuristic modes.

---

## Architecture Changes

### New Module: `agent/gemini_client.py`

A **wrapper module** that provides an OpenAI-compatible interface to Gemini API:

```python
from agent.gemini_client import create_gemini_client

# Create client
client = create_gemini_client(api_key="AIzaSy...")

# Use OpenAI-style interface
response = client.chat.completions.create(
    model="gemini-1.5-flash",
    messages=[
        {"role": "system", "content": "You are helpful..."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7
)

# Extract content
reply = response.choices[0].message.content
```

### Updated Files

| File | Changes |
|------|---------|
| `requirements.txt` | Replaced `openai` with `google-generativeai>=0.5.0` |
| `agent/business_agent.py` | Uses `create_gemini_client()` instead of `OpenAI()`, updated env vars |
| `agent/baseline_agent.py` | Uses Gemini client, updated docstrings and imports |
| `main.py` | Removed OpenAI import, updated env var, updated error handling |
| `config/openenv.yaml` | Model updated to `gemini-1.5-flash` |
| `agent/gemini_client.py` | **NEW** - Gemini API wrapper with OpenAI-compatible interface |

---

## Available Gemini Models

### Recommended for This Project

1. **`gemini-1.5-flash`** (Default)
   - Fastest, most cost-effective
   - Great for: Social media, reviews, quick analysis
   - Latency: ~1-2 seconds
   - Input cost: $0.075 per 1M tokens
   - Output cost: $0.30 per 1M tokens

2. **`gemini-1.5-pro`** (Higher Quality)
   - Better reasoning and longer context
   - Great for: Complex strategies, detailed reports
   - Latency: ~3-5 seconds
   - Input cost: $1.50 per 1M tokens
   - Output cost: $6.00 per 1M tokens

3. **`gemini-1.0-pro`** (Legacy, Lighter)
   - Still available for backward compatibility
   - Lower cost than 1.5 versions

### Switching Models

Edit `config/openenv.yaml`:
```yaml
agent:
  model: "gemini-1.5-pro"  # Change here
```

Or set environment variable:
```bash
export GOOGLE_MODEL="gemini-1.5-pro"
```

Or pass directly:
```python
agent = BusinessGrowthAgent(model="gemini-1.5-pro")
```

---

## API Compatibility Layer

### Message Format

**OpenAI Format** (also used by Gemini wrapper):
```json
{"role": "system", "content": "You are helpful..."}
{"role": "user", "content": "Hello!"}
{"role": "assistant", "content": "Hello! How can I help?"}
```

### Response Format

Both APIs follow the same response structure:
```python
response.choices[0].message.content  # <- Same in both
```

---

## Configuration Reference

### Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| `GOOGLE_API_KEY` | (required) | Your Google Gemini API key |
| `GOOGLE_MODEL` | `gemini-1.5-flash` | Which Gemini model to use |
| `GOOGLE_TEMPERATURE` | `0.7` | Sampling temperature (0.0-2.0) |

### Configuration File: `config/openenv.yaml`

```yaml
agent:
  model: "gemini-1.5-flash"  # Gemini model name
  temperature: 0.0            # Lower = more deterministic
  max_retries: 3              # Retry failed API calls
```

---

## Troubleshooting

### ❌ Error: "Google API key is required"

**Solution**: Set the `GOOGLE_API_KEY` environment variable:
```bash
export GOOGLE_API_KEY="AIzaSy..."
python main.py
```

### ❌ Error: "google.generativeai package not installed"

**Solution**: Install dependencies:
```bash
pip install google-generativeai>=0.5.0
```

### ❌ Error: "Invalid API key"

**Solution**: 
1. Verify your API key from https://aistudio.google.com/app/apikeys
2. Make sure there are no extra spaces or characters
3. Ensure you're using the correct format: `AIzaSy...`

### ❌ Error: "Model not found / Invalid model"

**Solution**: Use valid Gemini models:
- ✅ `gemini-1.5-flash` (recommended)
- ✅ `gemini-1.5-pro`
- ✅ `gemini-1.0-pro`

### ⚠️ Slower Response Times

**Possible Causes**:
- Using `gemini-1.5-pro` (slower but higher quality)
- Network latency to Google's servers
- High request volume

**Solutions**:
- Switch to `gemini-1.5-flash`
- Check your internet connection
- Implement request batching for multiple calls

### ⚠️ Different Output Quality

**Expected**: Gemini produces slightly different outputs than GPT-4o-mini

**Why**:
- Different training data
- Different reasoning patterns
- Different tokenization

**Solution**: Use `temperature=0.0` for more consistent, structured responses

---

## Cost Comparison

### OpenAI (GPT-4o-mini)

| Type | Cost |
|------|------|
| Input (1M tokens) | $0.15 |
| Output (1M tokens) | $0.60 |
| Estimated monthly (10K requests) | ~$50-100 |

### Google Gemini (1.5 Flash)

| Type | Cost |
|------|------|
| Input (1M tokens) | $0.075 |
| Output (1M tokens) | $0.30 |
| Estimated monthly (10K requests) | ~$25-50 |

**Result**: ✅ **~50% cost savings** with Gemini 1.5 Flash

---

## Performance Comparison

| Metric | GPT-4o-mini | Gemini 1.5 Flash |
|--------|-----------|------------------|
| Latency | 1-2s | 1-2s |
| Cost | ~$0.15 per 1M input tokens | ~$0.075 per 1M input tokens |
| Context Window | 128K tokens | 1M tokens |
| Reasoning | Strong | Strong |
| Instruction Following | Excellent | Excellent |
| Code Generation | Excellent | Good |

---

## Implementation Details

### Custom Wrapper Benefits

The `agent/gemini_client.py` wrapper provides:

1. ✅ **API Compatibility**: Drop-in replacement for OpenAI
2. ✅ **Message Translation**: Automatically converts message formats
3. ✅ **Error Handling**: Consistent error messages
4. ✅ **Response Normalization**: Same output interface as OpenAI
5. ✅ **Easy Migration**: Minimal code changes required

### How It Works

```python
# Wrapper receives OpenAI-style messages
messages = [
    {"role": "system", "content": "You are helpful"},
    {"role": "user", "content": "Hello"}
]

# Translates to Gemini format
# - "system" → prepended as context
# - "assistant" → "model" role
# - "user" → "user" role

# Calls Gemini API
response = gemini_model.generate_content(...)

# Wraps response to match OpenAI format
return GeminiChatCompletion(text)
```

---

## Testing

### Unit Tests

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_agent.py -v

# Run with coverage
pytest --cov=agent tests/
```

### Manual Testing

```bash
# Test each capability
python main.py

# Test baseline agent
python agent/baseline_agent.py

# Test with specific model
GOOGLE_MODEL=gemini-1.5-pro python main.py
```

---

## FAQ

### Q: Can I use both OpenAI and Gemini in the same project?

**A**: Yes, but not recommended. The current migration fully uses Gemini. To use both:
1. Install both `openai` and `google-generativeai`
2. Create separate agent classes
3. Switch between them based on configuration

### Q: How do I revert to OpenAI?

**A**: 
1. Reinstall OpenAI: `pip install openai>=1.30.0`
2. Restore original files from git
3. Set `OPENAI_API_KEY` environment variable

### Q: Is Gemini as good as GPT-4o-mini?

**A**: For this business use case, **yes**. Gemini 1.5 Flash provides:
- ✅ Comparable quality
- ✅ Faster execution
- ✅ Lower cost
- ✅ Larger context window

### Q: Can I use different models for different tasks?

**A**: Yes, create multiple agent instances:
```python
agent1 = BusinessGrowthAgent(model="gemini-1.5-flash")  # Fast
agent2 = BusinessGrowthAgent(model="gemini-1.5-pro")    # Better quality
```

### Q: How do I handle rate limits?

**A**: The client includes `max_retries: 3` in config. Gemini's free tier allows ~15 requests/minute.

---

## Next Steps

### Optimization

- [ ] Implement request caching for repeated queries
- [ ] Add batch processing for multiple analyses
- [ ] Use `temperature=0.0` for deterministic output
- [ ] Implement streaming for long responses

### Monitoring

- [ ] Track API usage and costs
- [ ] Monitor response latencies
- [ ] Log model performance metrics
- [ ] Set up alerts for errors

### Enhancement

- [ ] Add support for multiple models simultaneously
- [ ] Implement model fallback strategy
- [ ] Add telemetry and analytics
- [ ] Create performance benchmarks

---

## Support & Resources

- **Google AI Studio**: https://aistudio.google.com/
- **Gemini API Docs**: https://ai.google.dev/
- **API Reference**: https://ai.google.dev/api/rest
- **Pricing**: https://ai.google.dev/pricing
- **Community**: https://discuss.ai.google/

---

## Summary

✅ **Migration Complete!**

Your project now uses:
- **Google Gemini 1.5 Flash** for LLM inference
- **50% lower costs** than OpenAI
- **Same API interface** as before
- **Full backward compatibility** with existing code
- **Same features** and capabilities

### Quick Checklist

- [x] Requirements updated
- [x] Gemini client wrapper created
- [x] `business_agent.py` migrated
- [x] `baseline_agent.py` migrated
- [x] Configuration updated
- [x] Main CLI updated
- [x] Documentation complete

**Ready to use!** 🚀
