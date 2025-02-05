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
$ conda create -n fpy python=3.12
$ conda activate fpy
$ poetry install
```

### Install Formula
```bash
$ dotnet tool install --global VUISIS.Formula.<x64|ARM64> 
```

### Set OpenAI Env 
Create a .env file in the root directory and set the environment variable OPENAI_API_KEY.
```
OPENAI_API_KEY=<your-openai-api-key>
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

### Run Jupyter Notebook
```bash
$ jupyter notebook
```