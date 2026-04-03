param(
    [switch]$RunTests
)

$ErrorActionPreference = 'Stop'

function Invoke-Step {
    param(
        [string]$Name,
        [scriptblock]$Command
    )

    Write-Host "`n=== $Name ===" -ForegroundColor Cyan
    & $Command
}

$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    $pythonCmd = "py -3"
} else {
    throw "Python is not installed or not on PATH."
}

Invoke-Step -Name "Install dependencies" -Command {
    Invoke-Expression "$pythonCmd -m pip install -r requirements.txt"
}

Invoke-Step -Name "Run baseline agent" -Command {
    Invoke-Expression "$pythonCmd agent/baseline_agent.py"
}

if ($RunTests) {
    Invoke-Step -Name "Run tests" -Command {
        Invoke-Expression "$pythonCmd -m pytest tests/ -v"
    }
}

Write-Host "`nDone." -ForegroundColor Green
