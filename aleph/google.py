import os

google_api_key = os.environ.get("GOOGLE_API_KEY")
google_search_engine_id = os.environ.get("GOOGLE_SEARCH_ENGINE_ID")

google_search_url = "https://www.googleapis.com/customsearch/v1"


async def search(client, query: str):
    response = await client.get(
        google_search_url,
        params={
            "key": google_api_key,
            "cx": google_search_engine_id,
            "q": query,
        },
    )
    return [item["link"] for item in response.json()["items"]]
