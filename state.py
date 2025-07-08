from typing import TypedDict, List , Optional

class AgentState(TypedDict):
    text:str
    classification:Optional[str]
    entities:Optional[List[str]]
    summary:Optional[str]
    memory: Optional[List[str]] 