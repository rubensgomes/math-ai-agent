# Ollama LLM Models

This file describes the steps to install and run Ollama with open source (FREE)
LLM models locally. For more information about `Ollama` go
to [Ollama](https://ollama.ai/).

## Prerequisites

- Ubuntu 24.04.4 LTS
- Sudo privileges

## Install Ollama

- Install Ollama in Ubuntu Linux:

    ```bash
    # zstd is required
    sudo apt-get install zstd
    curl -fsSL https://ollama.com/install.sh | sh
    ```

## Popular Open-Source Models

### LLaMA 2 (Meta)

| Model        | Size | RAM Required | Description                 |
|--------------|------|--------------|-----------------------------|
| `llama2`     | 7B   | ~8GB RAM     | General-purpose             |
| `llama2:13b` | 13B  | ~16GB RAM    | Better quality, more memory |
| `llama2:70b` | 70B  | ~64GB RAM    | Highest quality             |

### Mistral

| Model              | Size | RAM Required | Description           |
|--------------------|------|--------------|-----------------------|
| `mistral`          | 7B   | ~8GB RAM     | Excellent performance |
| `mistral-openorca` | 7B   | ~8GB RAM     | Enhanced reasoning    |

### Phi

| Model  | Size | RAM Required | Description       |
|--------|------|--------------|-------------------|
| `phi`  | 2.7B | ~4GB RAM     | Lightweight, fast |
| `phi3` | 3.8B | ~6GB RAM     | Improved version  |

### Other Popular Models

```bash
# Download and run models
ollama pull llama2          # LLaMA 2 7B
ollama pull mistral        # Mistral 7B
ollama pull phi            # Phi 2.7B
ollama pull phi3           # Phi 3
ollama pull neural-chat    # Neural Chat
ollama pull orca2          # Orca 2
ollama pull codellama      # Code-focused
ollama pull llava          # Vision + Text
```

## Download a Model

```bash
# Pull a model to your local system
ollama pull llama2

# Or run directly (will download automatically)
ollama run llama2
```

## Removing a Model from Ollama

You can remove models using the `ollama rm` command.

### Remove a Specific Model

```bash
# Remove a specific model
ollama rm minimax-m2.5:cloud
```

### Remove Multiple Models

```bash
# Remove multiple models at once
ollama rm mistral llama2 phi3
```

### Verify Removal

```bash
# List remaining models
ollama list
```

### Other Useful Commands

```bash
# Remove all unused models
ollama prune

# Show model details before removing
ollama show minimax-m2.5:cloud
```

### Example Output

```bash
$ ollama rm minimax-m2.5:cloud
Deleted 'minimax-m2.5:cloud'

$ ollama list
NAME    ID          SIZE    MODIFIED
```

### Note

- Removing a model frees up disk space
- You can always re-download a model later with `ollama pull <model-name>`

## System Requirements (Approximate)

| Model Size | Minimum RAM | Recommended |
|------------|-------------|-------------|
| 3B         | 6GB         | 8GB         |
| 7B         | 8GB         | 16GB        |
| 13B        | 16GB        | 24GB        |
| 34B        | 32GB        | 48GB        |
| 70B        | 64GB        | 128GB       |

## Recommended Starting Models

1. **For beginners**: `phi` or `mistral` (lightweight, fast)
2. **For balance**: `mistral` or `llama2` (good quality, reasonable size)
3. **For coding**: `codellama` (specialized for code)
4. **For reasoning**: `mistral-openorca`

## Check Available Models

```bash
# See all available models online
ollama list

# Search for specific models
ollama search llama
```
