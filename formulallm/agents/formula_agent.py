import os

from langchain.chat_models import ChatOpenAI
from langchain.agents.agent import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.memory import ConversationBufferMemory

from .formula_tools import FormulaCodeLLM
from .prompts import FIX_CODE_PREFIX, QUERY_PROMPT

class FormulaAgent:
    def __init__(self, model="gpt-3.5-turbo-0125", temperature=0.0):
        if not os.environ["OPENAI_API_KEY"]:
            raise ValueError("Environment variable OPENAI_API_KEY is not set.")
        
        self.llm = ChatOpenAI(temperature=temperature, model=model)

        system_message = SystemMessage(content=FIX_CODE_PREFIX)
        _prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

        tools = [FormulaCodeLLM(name="formulallm", description="Formula llm", llm=self.llm)]

        agent = OpenAIFunctionsAgent(
            llm=self.llm,
            prompt=_prompt,
            tools=tools,
            memory=memory
        )

        self.agent_executor = AgentExecutor.from_agent_and_tools(
                agent=agent,
                tools=tools,
                verbose=True,
        )

    def run(self, code, prompt):
        prompts = QUERY_PROMPT.format(code=code, prompt=prompt)
        prompts.encode('unicode_escape')
        self.agent_executor.run(prompts)