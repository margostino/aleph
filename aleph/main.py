import asyncio

from aleph.config import parse_args
from aleph.file_data_collector import get_files_content
from aleph.llm import get_decision_making_helper
from aleph.web_collector import get_web_information


async def main():
    args = parse_args()
    query = args.query
    files_content = get_files_content()
    search_results = await get_web_information(query)

    decision_making_helper_result = get_decision_making_helper(
        query, search_results, files_content
    )
    print("\n\n\n")
    print(decision_making_helper_result)
    print("\n\n\n")


asyncio.run(main())
