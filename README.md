# FORMULA LLM - LLM Explanation and Repair

### Requirements
```bash
python = 3.10
dotnet 6.0
poetry 
```

### Python dependencies
```bash
Dependencies are listed in pyproject.toml under [tool.poetry.dependencies]
```

### Install poetry 
```bash
// Linux, macOS, and Windows (WSL)
$ curl -sSL https://install.python-poetry.org | python3 -

// Windows (Powershell)
$ (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

### Create conda environment
```bash
$ conda create -n fpy python=3.10
$ conda activate fpy
$ poetry install
```

### Install Formula
```bash
$ dotnet tool install --global VUISIS.Formula.<x64|ARM64> 
```

### Set OpenAI Env (optional)
```bash
Set the environment variable OPENAI_API_KEY if using GPT before running.
```