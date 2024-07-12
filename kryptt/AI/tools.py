# Local Imports
from config import OPENAI_TOKEN, OPENROUTER_TOKEN
from validation import AIInput

# Langchain
from langchain.tools import StructuredTool

# Phidata
from phi.assistant.python import PythonAssistant
from phi.llm.openai import OpenAIChat

from langchain.agents import Tool
from langchain_experimental.utilities import PythonREPL

# TODO Implement a E2B Python Tool instead of repl or phi data


python_repl = PythonREPL()
# You can create the tool to pass to an agent
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)


# Python Tool
python_assistant = PythonAssistant(
    llm=OpenAIChat(model="gpt-3.5-turbo", api_key=OPENAI_TOKEN),
    pip_install=True,
    show_function_calls=True,
    run_code=True,
    save_and_run=True,
    run_files=True,
    instructions=["Always use logger to showcase print statements"]
)

python_assistant_tool = StructuredTool.from_function(
    func=python_assistant.print_response,
    description="A Python shell. Used for data analysis, predictions and machine learning. Use this to execute python commands. Input should be a valid python command. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`",
    name="python_assistant",
    args_schema=AIInput
)