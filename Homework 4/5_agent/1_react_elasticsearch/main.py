import asyncio
import json
from typing import Annotated, Literal

import requests
from dotenv import load_dotenv
from langchain_core.messages import ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

from visualizer import visualize

load_dotenv()

# ============================================================================
# ELASTICSEARCH CONNECTION
# ============================================================================

ES_URL = "http://localhost:9200"
ES_HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}


def es_search(index: str, body: dict, timeout: int = 30) -> dict:
    """Execute an Elasticsearch search via plain HTTP (version-agnostic)."""
    response = requests.post(
        f"{ES_URL}/{index}/_search",
        json=body,
        headers=ES_HEADERS,
        timeout=timeout,
    )
    response.raise_for_status()
    return response.json()


def es_ping() -> bool:
    """Check if Elasticsearch is reachable."""
    try:
        r = requests.get(ES_URL, headers=ES_HEADERS, timeout=5)
        return r.status_code == 200
    except Exception:
        return False

# ============================================================================
# MODEL
# ============================================================================

llm = ChatOpenAI(model="gpt-4o-mini")

# ============================================================================
# TOOLS
# ============================================================================


@tool
def search_products(query: str, max_results: int = 5) -> str:
    """
    Search for products in the Elasticsearch e-commerce index.
    Use this tool to find products matching a user's query by name, description, category, or brand.

    Args:
        query: The search query string (product name, category, brand, keywords, etc.)
        max_results: Maximum number of results to return (default: 5)

    Returns:
        A JSON string containing matching products with their details.
    """
    try:
        response = es_search(
            index="products",
            body={
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": ["name^3", "description", "category^2", "brand^2"],
                        "fuzziness": "AUTO",
                    }
                },
                "size": max_results,
                "_source": [
                    "name",
                    "description",
                    "category",
                    "brand",
                    "price",
                    "rating",
                    "review_count",
                    "stock_quantity",
                ],
            },
        )

        hits = response["hits"]["hits"]
        total = response["hits"]["total"]["value"]

        if not hits:
            return json.dumps({"total": 0, "results": [], "message": "No products found."})

        results = []
        for hit in hits:
            source = hit["_source"]
            results.append(
                {
                    "id": hit["_id"],
                    "score": round(hit["_score"], 3),
                    **source,
                }
            )

        return json.dumps({"total": total, "results": results}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_product_categories() -> str:
    """
    Get a list of all available product categories in the Elasticsearch index.
    Use this tool when the user asks about what categories or types of products are available.

    Returns:
        A JSON string with all unique categories and the number of products in each.
    """
    try:
        response = es_search(
            index="products",
            body={
                "size": 0,
                "aggs": {
                    "categories": {
                        "terms": {"field": "category.keyword", "size": 50}
                    }
                },
            },
        )

        buckets = response["aggregations"]["categories"]["buckets"]
        categories = [{"category": b["key"], "count": b["doc_count"]} for b in buckets]
        return json.dumps({"categories": categories}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


@tool
def get_products_by_price_range(min_price: float, max_price: float, max_results: int = 5) -> str:
    """
    Search for products within a specific price range.
    Use this tool when the user wants products within a budget or asks for cheap/expensive items.

    Args:
        min_price: Minimum price (inclusive)
        max_price: Maximum price (inclusive)
        max_results: Maximum number of results to return (default: 5)

    Returns:
        A JSON string containing products within the given price range.
    """
    try:
        response = es_search(
            index="products",
            body={
                "query": {
                    "range": {"price": {"gte": min_price, "lte": max_price}}
                },
                "sort": [{"rating": {"order": "desc"}}],
                "size": max_results,
                "_source": [
                    "name",
                    "category",
                    "brand",
                    "price",
                    "rating",
                    "review_count",
                    "stock_quantity",
                ],
            },
        )

        hits = response["hits"]["hits"]
        total = response["hits"]["total"]["value"]

        if not hits:
            return json.dumps({"total": 0, "results": [], "message": "No products found in that price range."})

        results = [{"id": hit["_id"], **hit["_source"]} for hit in hits]
        return json.dumps({"total": total, "results": results}, indent=2)

    except Exception as e:
        return json.dumps({"error": str(e)})


# ============================================================================
# LANGGRAPH DEFINITION
# ============================================================================

all_tools = [search_products, get_product_categories, get_products_by_price_range]


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    llm_with_tools = llm.bind_tools(all_tools)
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


class BasicToolNode:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {t.name: t for t in tools}

    async def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")

        outputs = []
        for tool_call in message.tool_calls:
            tool_result = await self.tools_by_name[tool_call["name"]].ainvoke(
                tool_call["args"]
            )
            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result) if not isinstance(tool_result, str) else tool_result,
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        return {"messages": outputs}


def route_tools(state: State) -> Literal["tools", "__end__"]:
    """Route to tools node if the last AI message has tool calls, otherwise end."""
    if isinstance(state, list):
        ai_message = state[-1]
    elif messages := state.get("messages", []):
        ai_message = messages[-1]
    else:
        raise ValueError(f"No messages found in input state: {state}")

    if hasattr(ai_message, "tool_calls") and len(ai_message.tool_calls) > 0:
        print("Routing to tools:", [tc["name"] for tc in ai_message.tool_calls])
        return "tools"
    return "__end__"


# ============================================================================
# MAIN
# ============================================================================


async def main():
    """Build and run the LangGraph ReAct agent with Elasticsearch tools."""

    # Check Elasticsearch connectivity
    print(f"Connecting to Elasticsearch at {ES_URL}...")
    if es_ping():
        print("Elasticsearch is reachable.\n")
    else:
        print(f"WARNING: Cannot reach Elasticsearch at {ES_URL}. Make sure it is running.\n")

    tool_node = BasicToolNode(tools=all_tools)

    # Build graph
    graph_builder = StateGraph(State)
    graph_builder.add_node("chatbot", chatbot)
    graph_builder.add_node("tools", tool_node)

    graph_builder.add_conditional_edges(
        "chatbot",
        route_tools,
        {"tools": "tools", "__end__": "__end__"},
    )
    graph_builder.add_edge("tools", "chatbot")
    graph_builder.set_entry_point("chatbot")

    graph = graph_builder.compile()

    # Visualize
    visualize(graph, "graph.png")

    print("E-commerce Search Agent ready!")
    print("Example queries:")
    print("  - 'Find me laptops under $1000'")
    print("  - 'What categories of products do you have?'")
    print("  - 'Show me top-rated headphones'")
    print("  - 'I'm looking for Nike shoes'\n")

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["quit", "exit", "q"]:
            print("Goodbye!")
            break

        async for event in graph.astream({"messages": ("user", user_input)}):
            for value in event.values():
                last_msg = value["messages"][-1]
                if last_msg.content:
                    print("Assistant:", last_msg.content)


if __name__ == "__main__":
    asyncio.run(main())
