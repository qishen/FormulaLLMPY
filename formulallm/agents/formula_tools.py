from typing import Any

from langchain.chat_models.base import BaseChatModel
from langchain.tools.base import BaseTool
from .prompts import (
    QUERY_PROMPT,
    OUTPUT_RETURN,
    FORMULA_CODE_LLM_DESC
)
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.tools import BaseTool

class FormulaCodeLLM(BaseTool):
    name = "FormulaCodeLLM"
    description = FORMULA_CODE_LLM_DESC
    llm: BaseChatModel

    def _run(self, arg, **kwargs) -> Any:
        prompt = kwargs["prompt"]
        code = kwargs["code"]
        output = kwargs["output"]

        explain_template = QUERY_PROMPT
        
        prompt_template = PromptTemplate(
            input_variables=["prompt", "code", "output"],
            template=explain_template,
        )
        
        code_understander_chain = LLMChain(
            llm=self.llm, prompt=prompt_template, output_key="explanation"
        )

        out = code_understander_chain(kwargs)

        return_output = OUTPUT_RETURN.format(explanation=out['explanation'])

        return return_output

    async def _arun(
        self,
    ):
        raise NotImplementedError("custom_search does not support async")