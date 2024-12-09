from typing import Optional

from pydantic import BaseModel


class SearchResultSummary(BaseModel):
    link: str
    summary: Optional[str]
    reasoning: str


def prompt():
    return """
Your are a great Web Scrapper. You are given a script result of a browser search and your job is to transform it in an structured information removing the non-important part and extracting the relevant parts.

If the content is not relevant to the query, you should not return summary. Also you should always return a reasoning.

Your output should be based on the schema I provide you.
  """
