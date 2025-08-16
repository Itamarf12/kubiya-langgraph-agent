# Kubiya LangGraph Research Agent

## Overview

The Kubiya LangGraph Research Agent is an intelligent, automated research assistant that helps developers and researchers explore GitHub repositories on specific topics. Using LangGraph and LangChain, the agent performs a comprehensive research workflow that includes:

- **GitHub Repository Discovery**: Searches for relevant repositories based on your topic
- **Repository Analysis**: Enriches repository data with contributor information and metadata
- **Intelligent Planning**: Generates structured research plans using AI to guide your exploration
- **Error Handling**: Gracefully handles common issues like no results, API limits, and network problems

The agent is particularly useful for:
- Researching new technologies or frameworks
- Finding the best open-source projects in a domain
- Understanding community activity and contributor patterns
- Creating systematic exploration plans for complex topics

## Features

- 🔍 **Smart GitHub Search**: Finds repositories by name and description
- 📊 **Repository Enrichment**: Gathers stars, contributors, languages, and update dates
- 🤖 **AI-Powered Planning**: Generates step-by-step research plans using GPT-4
- 🛡️ **Robust Error Handling**: Continues working even when encountering issues
- 📝 **Structured Output**: Provides clear, actionable research plans in Markdown format

## Prerequisites

- **Python 3.8+** (3.9+ recommended)
- **OpenAI API Key** for GPT-4 access
- **GitHub Personal Access Token** (optional, but recommended for higher rate limits)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Itamarf12/-kubiya-langgraph-agent.git
cd kubiya-langgraph-agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don't have a requirements.txt file, install the required packages manually:

```bash
pip install langgraph langchain langchain-openai requests
```

### 3. Set Up API Keys

#### OpenAI API Key (Required)

You need an OpenAI API key to use the GPT-4 model for generating research plans.

**Option A: Environment Variable (Recommended)**
```bash
export OPENAI_API_KEY="sk-your-openai-api-key-here"
```

**Option B: Command Line Parameter**
```bash
python3 src/main_agent/py "your topic"
```

#### GitHub Token (Optional but Recommended)

A GitHub Personal Access Token increases your API rate limits from 60 to 5000 requests per hour.

1. Go to [GitHub Settings > Developer settings > Personal access tokens](https://github.com/settings/tokens)
2. Generate a new token with `public_repo` scope
3. Set it as an environment variable:

```bash
export GITHUB_TOKEN="ghp_your_github_token_here"
```

Or update the `GITHUB_TOKEN` variable in `src/graph.py`:

```python
GITHUB_TOKEN = "ghp_your_github_token_here"  # Replace with your actual token
```

## Usage

### Basic Usage

```bash
# Run with a topic
python3 src/main_agent.py "machine learning"

```

### Programmatic Usage

```python
from src.main_agent import run_research_agent

# Run the agent programmatically
run_research_agent("vector database")
```

### Example Topics to Try

- "vector database"
- "machine learning framework"
- "web framework"
- "data visualization"
- "blockchain"
- "game engine"

## Example Output

Here's what you can expect when running the agent on "vector database":

```markdown
# Research Plan for: vector database

## Summary
Found 5 high-quality vector database repositories with active development and strong community support.

## Exploration Steps

### 1. **Start with Pinecone** ⭐⭐⭐⭐⭐
- **Repository**: pinecone-io/pinecone-python
- **Stars**: 4.2k+
- **Language**: Python
- **Focus**: Managed vector database service
- **Action**: Read the quickstart guide and explore the Python client documentation

### 2. **Explore Weaviate** ⭐⭐⭐⭐⭐
- **Repository**: weaviate/weaviate
- **Stars**: 6.8k+
- **Language**: Go
- **Focus**: Vector search engine with GraphQL API
- **Action**: Check out the getting started tutorial and API reference

### 3. **Investigate Qdrant** ⭐⭐⭐⭐
- **Repository**: qdrant/qdrant
- **Stars**: 12.5k+
- **Language**: Rust
- **Focus**: Vector similarity search engine
- **Action**: Review the Rust client examples and performance benchmarks

### 4. **Compare Features**
- **Vector Operations**: Compare CRUD operations across platforms
- **Scalability**: Review deployment options and clustering capabilities
- **Integrations**: Check available client libraries and frameworks
- **Performance**: Look for benchmark results and optimization guides

### 5. **Community Analysis**
- **Contributor Activity**: Review recent commits and issue responses
- **Documentation Quality**: Assess tutorials, examples, and API docs
- **Ecosystem**: Check for related tools, plugins, and integrations

## Next Steps
1. Set up development environments for your top 2-3 choices
2. Run through quickstart tutorials
3. Build a simple proof-of-concept application
4. Evaluate performance and ease of use for your specific use case
```

## Configuration

### Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-your-openai-api-key"

# Optional but recommended
export GITHUB_TOKEN="ghp_your_github_token"
```

## Project Structure

```
kubiya-langgraph-agent/
├── src/
│   ├── __init__.py
│   ├── main_agent.py      # Main entry point
│   ├── graph.py           # LangGraph workflow definition
│   └── state.py           # State management and data structures
├── README.md
└── requirements.txt
```

## How It Works

1. **GitHub Search**: Queries GitHub's search API for repositories matching your topic
2. **Repository Enrichment**: Fetches additional metadata including contributors and activity
3. **AI Analysis**: Uses GPT-4 to analyze the repositories and generate a research plan
4. **Output Generation**: Produces a structured Markdown plan with actionable steps

## Error Handling

The agent gracefully handles common issues:

- **No Results**: Provides suggestions for alternative search terms
- **API Rate Limits**: Offers guidance on using GitHub tokens
- **Network Issues**: Suggests troubleshooting steps
- **Invalid Queries**: Recommends reformulating search terms

