import os
from typing import List, Annotated, TypedDict
from typing_extensions import TypedDict
from dotenv import load_dotenv

from langchain.agents import AgentExecutor, create_react_agent
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_deepseek import ChatDeepSeek
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages

from formulallm.agents.prompts import *

class State(TypedDict):
    # Messages have the type "list". The `add_messages` function
    # in the annotation defines how this state key should be updated
    # (in this case, it appends messages to the list, rather than overwriting them)
    messages: Annotated[list, add_messages]

class FormulaLLMAgent:
    def __init__(self, model="deepseek-coder", temperature=0.0):
        load_dotenv()
        
        if "deepseek" in model:
            if not os.getenv("DEEPSEEK_API_KEY"):
                raise ValueError("DEEPSEEK_API_KEY not found in .env file or environment variables")
            self.llm = ChatDeepSeek(temperature=temperature, model=model)
        else:
            if not os.getenv("OPENAI_API_KEY"):
                raise ValueError("OPENAI_API_KEY not found in .env file or environment variables")
            self.llm = ChatOpenAI(temperature=temperature, model=model)

    def run(self, prompt: str,files: List[str]) -> None:
        print("Starting conversation with the agent. Type 'exit' to end the session.")

        def chatbot(state: State):
            return {"messages": [self.llm.invoke(state["messages"])]}

        graph_builder = StateGraph(State)
        graph_builder.add_node("chatbot", chatbot)
        graph_builder.add_edge(START, "chatbot")
        graph_builder.add_edge("chatbot", END)
        graph = graph_builder.compile()

        def stream_graph_updates(user_input: str):
            for event in graph.stream({"messages": [
                {"role": "user", "content": user_input},
                {"role": "system", "content": ",".join(files)}
            ]}):
                for value in event.values():
                    print("Assistant:", value["messages"][-1].content)

        print("Getting back results from initial prompt...")
        stream_graph_updates(prompt)

        while True:
            try:
                user_input = input("User: ")
                if user_input.lower() in ["quit", "exit", "q"]:
                    print("Goodbye!")
                    break
                print("Start reasoning and generating code again...")
                stream_graph_updates(user_input)
            except:
                # fallback if input() is not available
                user_input = "What do you know about LangGraph?"
                print("User: " + user_input)
                stream_graph_updates(user_input)
                break