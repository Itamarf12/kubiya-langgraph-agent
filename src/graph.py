import os
from langgraph.graph import StateGraph, END
from langchain_core.prompts import ChatPromptTemplate
from state import AgentState
from langchain.chat_models import init_chat_model
import requests


# Optional: Provide a GitHub Personal Access Token to increase API rate limits
GITHUB_TOKEN = None  # e.g., "ghp_your_token"
HEADERS = {
    "Accept": "application/vnd.github+json",
}
if GITHUB_TOKEN:
    HEADERS["Authorization"] = f"Bearer {GITHUB_TOKEN}"


# LLM setup
llm = init_chat_model("openai:gpt-4.1")


def github_search_node(state: AgentState):
    """
    Search GitHub for repositories related to the given topic.
    Returns a list of basic repo info.
    """
    topic = state.get("topic")
    max_repos = 5
    query = f"{topic} in:name,description"
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={max_repos}"

    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        return {
            "repositories": [],
            "error": f"GitHub API error: {response.status_code} - {response.text}"
        }

    items = response.json().get("items", [])
    if not items:
        return {
            "repositories": [],
            "error": f"No repositories found for topic '{topic}'. Try broadening your search terms or checking the spelling."
        }

    return {"repositories" : items}


def get_top_contributors(repo_full_name: str, max_contributors: int = 3):
    """
    Fetch top contributors for a given repository.
    Returns a list of contributor usernames and their contribution count.
    """
    url = f"https://api.github.com/repos/{repo_full_name}/contributors?per_page={max_contributors}"
    response = requests.get(url, headers=HEADERS, timeout=10)
    if response.status_code != 200:
        print(f"⚠️  Could not fetch contributors for {repo_full_name}")
        return []

    contributors = response.json()
    return [
        {"username": c["login"], "contributions": c["contributions"]}
        for c in contributors
    ]


def enrich_contributors_node(state: AgentState):
    """
    Extracts relevant metadata from a list of GitHub repository items.
    """
    enriched_data = []
    repos = state.get("repositories")

    # Check if we have repositories to process
    if not repos:
        error = state.get("error", "No repositories available for processing.")
        return {
            "enriched_repos": [],
            "error": error,
            "plan": f"# Research Plan for: {state.get('topic')}\n\n## Summary\n\n{error}\n\n## Recommendations\n\n- Try using different search terms\n- Check if the topic name is spelled correctly\n- Consider broader or more specific keywords\n- Verify the topic exists in the GitHub ecosystem"
        }

    for repo in repos:
        repo_data = {
            "name": repo["full_name"],
            "url": repo["html_url"],
            "stars": repo["stargazers_count"],
            "description": repo["description"],
            "last_updated": repo["updated_at"],
            "language": repo["language"],
        }

        contributors = get_top_contributors(repo["full_name"])
        repo_data["top_contributors"] = contributors

        enriched_data.append(repo_data)

    return {"enriched_repos": enriched_data}


def plan_generation_node(state: AgentState):
    """
    Uses an LLM to generate a markdown exploration plan from metadata.
    """
    topic = state.get("topic")
    enriched_repos = state.get("enriched_repos")
    if not enriched_repos:
        error = state.get("error", "No repository data available for plan generation.")
        return {
            "plan": f"# Research Plan for: {topic}\n\n## Summary\n\n{error}\n\n## Recommendations\n\n- Try searching with different keywords\n- Check your internet connection\n- Verify the topic exists in the GitHub ecosystem\n- Consider using more specific or broader search terms"
        }

    # Format repo metadata as input to LLM
    repo_summaries = ""
    for i, repo in enumerate(enriched_repos, 1):
        repo_summaries += (
            f"### {i}. {repo['name']}\n"
            f"- Stars: {repo['stars']}\n"
            f"- Description: {repo['description']}\n"
            f"- Last Updated: {repo['last_updated']}\n"
            f"- Top Contributors: {', '.join(c['username'] for c in repo['top_contributors'])}\n"
            f"- URL: {repo['url']}\n\n"
        )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a technical research assistant helping users explore GitHub projects.",
        ),
        (
            "user",
            f"""Given the topic: **{topic}** and the following repository metadata:

    {repo_summaries}

    Generate a clear, step-by-step exploration plan in Markdown format.
    Each step should recommend specific actions like reading docs, comparing features, or exploring contributors."""
        )
    ])

    chain = prompt | llm
    return {"plan": chain.invoke({}).content}


# Graph definition
def create_git_graph() -> StateGraph:
    """
    Defines and compiles the LangGraph workflow.
    """
    workflow = StateGraph(AgentState)

    # Add nodes to the graph
    workflow.add_node("github_search", github_search_node)
    workflow.add_node("enrich_contributors", enrich_contributors_node)
    workflow.add_node("plan_generation_node", plan_generation_node)

    # Define the flow (edges)
    workflow.set_entry_point("github_search")
    workflow.add_edge("github_search", "enrich_contributors")
    workflow.add_edge("enrich_contributors", "plan_generation_node")
    workflow.add_edge("plan_generation_node", END)

    return workflow.compile()