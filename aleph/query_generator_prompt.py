from typing import List

from pydantic import BaseModel


class QueriesByTopic(BaseModel):
    topic: str
    queries: List[str]


class QueryGenerator(BaseModel):
    queries_by_topic: List[QueriesByTopic]


def prompt(max_queries: int = 5, topics: list[str] = []):
    formatted_topics = "\n".join(f"• {topic}" for topic in topics) if topics else ""
    return f"""
Your are a internet searcher. You are given a query and you should suggest {max_queries} more queries per topic that might complement the original query and/or be more specific.
You should focus on these topics:
{formatted_topics}
Your output should be based on the schema I provide you.
  """
