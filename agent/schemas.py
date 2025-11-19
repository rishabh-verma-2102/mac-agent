from pydantic import BaseModel
from typing import List, Optional


class Function(BaseModel):
    name: str
    description: Optional[str] = None


class ToolCall(BaseModel):
    id: str
    type: str
    function: Function


class Message(BaseModel):
    role: str
    content: str
    tool_calls: Optional[ToolCall] = None
    tool_name: Optional[str] = None
