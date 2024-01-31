from langchain.chat_models import ChatOpenAI
import os
from langchain.agents.agent import AgentExecutor
from langchain.agents.openai_functions_agent.base import OpenAIFunctionsAgent
from langchain.schema.messages import SystemMessage
from langchain.memory import ConversationBufferMemory
from .formula_tools import FormulaCodeLLM
from .prompts import FIX_CODE_PREFIX, QUERY_PROMPT

if not os.environ["OPENAI_API_KEY"]:
    raise ValueError("Environment variable OPENAI_API_KEY is not set.")

llm = ChatOpenAI(temperature=0.0, model_name="gpt-3.5-turbo")

system_message = SystemMessage(content=FIX_CODE_PREFIX)
_prompt = OpenAIFunctionsAgent.create_prompt(system_message=system_message)

memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

tools = [FormulaCodeLLM(llm=llm)]

agent = OpenAIFunctionsAgent(
    llm=llm,
    prompt=_prompt,
    tools=tools,
    verbose=True,
    memory=memory
)

agent_executor = AgentExecutor.from_agent_and_tools(
        agent=agent,
        tools=tools,
        verbose=True,
)

def run_agent_executor(code, output, prompt):
    prompts = QUERY_PROMPT.format(code=code, output=output, prompt=prompt)
    prompts.encode('unicode_escape')
    agent_executor.run(prompts)