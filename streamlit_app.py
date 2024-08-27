from typing import Dict, Any

import streamlit as st
from langchain import hub
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_react_agent, create_tool_calling_agent
from langchain_community.callbacks import StreamlitCallbackHandler
from langchain_core.callbacks import StdOutCallbackHandler, BaseCallbackHandler
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory, StreamlitChatMessageHistory
from langchain_ollama import ChatOllama
from langchain.load.dump import dumps

from langchain_openai import ChatOpenAI
from prompts import appraisal_bot_prompt
from tools import *
from dotenv import load_dotenv

load_dotenv()

# llm = ChatOllama(temperature=0.5, model='llama3-groq-tool-use', model_kwargs={"seed": 42}, stream=True)
llm = ChatOpenAI(temperature=0, model='gpt-4o-mini')
tools = [mls_tool]

history = StreamlitChatMessageHistory()
model = llm.bind_tools(tools)
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            appraisal_bot_prompt
        ),
        ("placeholder", "{chat_history}"),
        ("placeholder", "{tools}"),
        ("placeholder", "{tool_names}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

agent = create_tool_calling_agent(model, tools, prompt)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    return_intermediate_steps=True,
    max_iterations=5,
)

agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: history,
    input_messages_key="input",
    history_messages_key="chat_history",
)


class MyCustomHandler(BaseCallbackHandler):

    def on_tool_end(self, output: str, **kwargs: Any) -> Any:
        """Run when tool ends running."""
        print(output)
        history.add_ai_message(f'tool_output: {output}')


avatars = {"human": "user", "ai": "assistant"}
for msg in history.messages:
    if not msg.content.__contains__("tool_output"):
        st.chat_message(avatars[msg.type]).write(msg.content)

if user_query := st.chat_input():
    st.chat_message("user").write(user_query)
    with st.chat_message("assistant"):
        callback = MyCustomHandler()
        st_callback = StreamlitCallbackHandler(st.container())
        response = (agent_with_chat_history.invoke({
            "input": user_query,
            "chat_history": history,
        }, {'configurable': {'session_id': 'placeholder_id'}, "callbacks": [st_callback, callback]}))
        st.write(response['output'].get(content, ""))
