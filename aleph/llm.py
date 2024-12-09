import os

from openai import OpenAI

from aleph.data_extractor_prompt import SearchResultSummary
from aleph.data_extractor_prompt import prompt as data_extractor_prompt
from aleph.decision_making_prompt import prompt as decision_making_prompt
from aleph.query_generator_prompt import QueryGenerator
from aleph.query_generator_prompt import prompt as query_generator_prompt

openai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


def get_search_result_summary(query: str, text: str):
    system_prompt = data_extractor_prompt()
    messages = [
        {"role": "user", "content": f"QUERY: {query}"},
        {"role": "user", "content": f"RESULT: {text.decode()}"},
    ]
    completion = openai_client.beta.chat.completions.parse(
        messages=[{"role": "system", "content": system_prompt}] + messages,
        model="gpt-4o",
        response_format=SearchResultSummary,
    )
    return completion.choices[0].message.parsed


def get_query_suggestions(query: str, search_topics: list[str]):
    system_prompt = query_generator_prompt(topics=search_topics)
    completion = openai_client.beta.chat.completions.parse(
        messages=[{"role": "system", "content": system_prompt}]
        + [{"role": "user", "content": query}],
        model="gpt-4o",
        response_format=QueryGenerator,
    )
    return completion.choices[0].message.parsed


def get_decision_making_helper(
    query: str, search_results: list[SearchResultSummary], additional_information: str
):
    system_prompt = decision_making_prompt()
    completion = openai_client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"QUERY: {query}"},
            {
                "role": "user",
                "content": f"SEARCH RESULTS: {[result.model_dump_json() for result in search_results]}",
            },
            {
                "role": "user",
                "content": f"ADDITIONAL INFORMATION: {additional_information}",
            },
        ],
        model="gpt-4o",
    )
    return completion.choices[0].message.content
