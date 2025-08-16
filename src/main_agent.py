import sys
from graph import create_git_graph
from state import AgentState


def run_research_agent(topic: str):
    """
    Initializes and runs the LangGraph research agent.
    """
    # Create the graph
    app = create_git_graph()

    # Initial state
    initial_state = AgentState(
        topic=topic,
        repositories=[],
        plan="",
        messages=[],
        error=None
    )

    print(f"Starting research on topic: '{topic}'...")
    print("---")

    # Run the graph and stream the output
    for state in app.stream(initial_state):
        print(state)
        print("---")

    final_state = next(iter(state.values()))

    print("FINAL RESEARCH PLAN:")
    print(final_state["plan"])
if __name__ == "__main__":
    if len(sys.argv) <1:
        print("Usage: python -m research_agent <topic>")
        sys.exit(1)

    topic = sys.argv[1]

    topic = "vector database"
    run_research_agent(topic)