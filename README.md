# FORMULA LLM - LLM Explanation and Repair

### Requirements
```
python = 3.10
dotnet 6.0
poetry 
```

### Python dependencies
```
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

### Set OpenAI Env 
```
Set the environment variable OPENAI_API_KEY if using agents module and GPT before running.
```

### Install Ollama For Local LLM
```bash
// Download Ollama for your platform here https://ollama.com/download if using pipelines module.

// Pull the LLM models
$ ollama pull mistral
$ ollama pull bakllava

// Run the Ollama server exe or by command
$ ollama serve
```