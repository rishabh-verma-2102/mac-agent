from typing import List, Sequence
from ollama import chat, ChatResponse
from agent.schemas import Message, ToolCall
from agent.tools import get_battery, get_disk, get_memory, get_cpu

system_prompt = (
    "You are a helpful assistant for MacBook hardware details. "
    "You have access to tools: 'get_battery', 'get_disk', 'get_memory', 'get_cpu'. "
    "\n\n"
    "### CRITICAL GUIDELINES:\n"
    "1. **Greetings:** If the user says 'hi', 'hello', or 'thanks', reply naturally in plain text. Do NOT call tools.\n"  # <--- NEW INSTRUCTION
    "2. **Tool Use:** Only use tools if the user asks for hardware information.\n"
    "3. **Format:** Never output empty JSON objects like '{}'. If you have nothing to say, ask the user what they need."
    "4. **NEVER** write JSON or simulated code in your text response to describe a tool call.\n"
    "5. **ALWAYS** use the native tool-calling capability provided to you if you need data.\n"
    "6. If the user asks for 'full details' or 'everything', call ALL relevant tools immediately.\n"
    "7. Do not describe what you are going to do. Just do it.\n"
)


class AgentService:
    TOOLS = [get_battery, get_disk, get_memory, get_cpu]

    def __init__(self):
        self.messages: List[Message] = [
            Message(role="system", content=system_prompt)
        ]
        self._tool_lookup = {func.__name__: func for func in self.TOOLS}

    def chat_agent(self, user_content: str):
        self.messages.append(Message(role="user", content=user_content))

        response: ChatResponse = self._chat_call()
        self.messages.append(response.message)

        if not response.message.tool_calls:
            return response.message.content

        loop_count = 0
        while response.message.tool_calls and loop_count < 5:
            tool_messages = self._tool_call_orchestrator(response.message.tool_calls)
            self.messages.extend(tool_messages)

            response = self._chat_call()
            self.messages.append(response.message)
            loop_count += 1

        return response.message.content

    def _tool_call_orchestrator(self, t: Sequence[ToolCall]):
        tool_messages: List[Message] = []
        for f in t:
            function_to_call = self._tool_lookup.get(f.function.name)

            if function_to_call and callable(function_to_call):
                try:
                    result = function_to_call()
                    tool_messages.append(Message(role="tool", content=str(result), tool_name=f.function.name))
                except Exception as e:
                    tool_messages.append(
                        Message(role="tool", content=f"Error executing tool: {e}", tool_name=f.function.name))
            else:
                tool_messages.append(
                    Message(role="tool", content=f"Function {f.function.name} not found.", tool_name=f.function.name))

        return tool_messages

    def _chat_call(self) -> ChatResponse:
        response: ChatResponse = chat(
            'llama3.1',
            messages=self.messages,
            tools=self.TOOLS,
        )
        return response
