from fastapi import APIRouter
from agent.service import AgentService

router = APIRouter()

agent_service = AgentService()


@router.post("/chat")
def chat_agent(message: str):
    return agent_service.chat_agent(user_content=message)
