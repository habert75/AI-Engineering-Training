# ReAct Elasticsearch Agent

A LangGraph ReAct agent that answers user queries by searching an Elasticsearch e-commerce product database.

## Architecture

```
User input → LangGraph chatbot node → (tool call?) → BasicToolNode → back to chatbot → response
```

**Tools available:**
- `search_products` — full-text search across product name, description, category, brand
- `get_product_categories` — lists all categories with product counts
- `get_products_by_price_range` — filters products by min/max price, sorted by rating

## Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager
- Docker Desktop with Elasticsearch running on `http://localhost:9200`
- OpenAI API key

## Setup

### 1. Start Elasticsearch

Start your Docker Desktop and ensure Elasticsearch is running:

```powershell
# Verify Elasticsearch is up
Invoke-RestMethod http://localhost:9200
```

### 2. Populate the database

The agent requires the `products` index to be populated. Run the populate script from the AI-Agents ecommerce project:

```powershell
Set-Location "C:\Users\jhabinshuti\OneDrive - vig.cz\Documents\IA\AI\AI-Agents\2_DB\2_ecommerce\3_Elasticsearch\scripts"
$env:PYTHONUTF8 = "1"
uv run --link-mode=copy python populate_data.py
```

Expected output: `products: 210 documents` (plus other indices).

### 3. Configure environment

Edit the `.env` file in this directory and set your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

### 4. Install dependencies

Because this project lives inside a OneDrive folder, the virtual environment must be created outside OneDrive to avoid file-lock errors:

```powershell
Set-Location "C:\Users\jhabinshuti\OneDrive - vig.cz\Documents\IA\AI\AI-Engineering-Training\Homework 4\5_agent\1_react_elasticsearch"
$env:UV_PROJECT_ENVIRONMENT = "C:\Temp\es-agent-venv"
uv sync
```

## Running the Agent

```powershell
Set-Location "C:\Users\jhabinshuti\OneDrive - vig.cz\Documents\IA\AI\AI-Engineering-Training\Homework 4\5_agent\1_react_elasticsearch"
$env:UV_PROJECT_ENVIRONMENT = "C:\Temp\es-agent-venv"
uv run python main.py
```

Type `quit`, `exit`, or `q` to stop.

## Example Queries

```
User: What categories of products do you have?
User: Show me top-rated headphones
User: Find me laptops under $1000
User: I'm looking for Nike shoes
User: What are the best products between $50 and $200?
```

## Project Structure

```
1_react_elasticsearch/
├── main.py          # Agent definition (LangGraph graph + Elasticsearch tools)
├── visualizer.py    # Saves graph diagram to graph.png
├── pyproject.toml   # Dependencies
├── .env             # API keys (not committed to git)
└── README.md        # This file
```
