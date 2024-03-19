FIX_CODE_PREFIX =  """ \
SYSTEM MESSAGE:

You are a computer scientist. You will be provided the assembly of a C++ program. You will explain why the program is broken and give solutions to fixing it.

END OF SYSTEM MESSAGE"""

QUERY_PROMPT = """ \
{prompt}

{code}
"""

OUTPUT_RETURN = """ \
{explanation}
"""

FORMULA_CODE_LLM_DESC = """ \
This is a Formula debugging tool. 

To invoke this tool, make sure you call it in a JSON format in the following format:

{
    "prompt": "FORMULA REQUEST HERE",
	"code": "FORMULA CODE HERE",
    "output": "FORMULA INTERPRETER OUTPUT HERE"
}

Make sure you only call this function with a JSON format, otherwise it will not work.
"""