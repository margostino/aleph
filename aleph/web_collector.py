import asyncio
import os

import httpx

from aleph.google import search
from aleph.llm import get_query_suggestions, get_search_result_summary
from aleph.query_generator_prompt import QueryGenerator

googgle_api_key = os.environ.get("GOOGLE_API_KEY")
google_search_engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")
google_search_url = "https://www.googleapis.com/customsearch/v1"

search_topics = ["competitors", "risks", "alternatives"]


async def extract_data_from_link(client, query, link):
    try:
        if not link.startswith(("http://", "https://")):
            print(f"Skipping link: {link}")
            return None
        async with client.stream("GET", link) as response:
            print(f"Fetching [{link}] for query [{query}]")
            text = await response.aread()
            completion_content = get_search_result_summary(query, text)
            return completion_content
    except Exception as e:
        print(f"Failed to fetch [{link}] for query [{query}]: {e}")
        return None


async def execute_query(client, query: str):
    links = await search(client, query)
    print(f"Executing query: '{query}'")
    tasks = [extract_data_from_link(client, query, link) for link in links]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]


async def get_web_information(initial_query: str):
    generated_queries: QueryGenerator = get_query_suggestions(
        initial_query, search_topics
    )
    all_queries = [
        query
        for queries_by_topic in generated_queries.queries_by_topic
        for query in queries_by_topic.queries
    ]
    # print queries by topic
    for queries_by_topic in generated_queries.queries_by_topic:
        print(f"Topic: {queries_by_topic.topic}")
        print("Queries:")
        for query in queries_by_topic.queries:
            print(f"- {query}")
        print("\n")

    async with httpx.AsyncClient(timeout=30.0) as client:
        tasks = [execute_query(client, query) for query in all_queries]
        results = await asyncio.gather(*tasks)

        flat_results = [
            item for sublist in results for item in sublist if item is not None
        ]
        for summary in flat_results:
            if summary.summary:
                print(
                    f"Link: {summary.link}\nReasoning: {summary.reasoning}\nSummary: {summary.summary}\n\n"
                )
        return flat_results
