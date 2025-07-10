from langchain.memory import ConversationBufferMemory
from langchain.chains.conversation.memory import ConversationBufferWindowMemory

memory_store = {}

def get_agent_memory(agent_name: str):
    if agent_name not in memory_store:
        memory_store[agent_name] = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
        )
    return memory_store[agent_name]
