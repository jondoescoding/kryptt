import os
import json
from config import E2B_API_KEY
from typing import Any, List
from langchain_core.tools import Tool
from pydantic.v1 import BaseModel, Field
from e2b_code_interpreter import CodeInterpreter
from langchain_core.messages import BaseMessage, ToolMessage
from langchain.agents.output_parsers.tools import (
    ToolAgentAction,
)


class LangchainCodeInterpreterToolInput(BaseModel):
    code: str = Field(description="Python code to execute.")


class CodeInterpreterFunctionTool:
    """
    This class calls arbitrary code against a Python Jupyter notebook.
    It requires an E2B_API_KEY to create a sandbox.
    """

    tool_name: str = "code_interpreter"

    def __init__(self):
        # Instantiate the E2B sandbox - this is a long lived object
        # that's pinging E2B cloud to keep the sandbox alive.
        self.code_interpreter = CodeInterpreter(api_key=E2B_API_KEY)

    def close(self):
        self.code_interpreter.close()

    def call(self, parameters: dict, **kwargs: Any):
        code = parameters.get("code", "")
        print(f"***Code Interpreting...\n{code}\n====")
        execution = self.code_interpreter.notebook.exec_cell(code)
        return {
            "results": execution.results,
            "stdout": execution.logs.stdout,
            "stderr": execution.logs.stderr,
            "error": execution.error,
        }

    # langchain does not return a dict as a parameter, only a code string
    def langchain_call(self, code: str):
        return self.call({"code": code})

    def to_langchain_tool(self) -> Tool:
        tool = Tool(
            name=self.tool_name,
            description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
            func=self.langchain_call,
        )
        tool.args_schema = LangchainCodeInterpreterToolInput
        return tool

    @staticmethod
    def format_to_tool_message(
        agent_action: ToolAgentAction,
        observation: dict,
    ) -> List[BaseMessage]:
        """
        Format the output of the CodeInterpreter tool to be returned as a ToolMessage.
        """
        new_messages = list(agent_action.message_log)

        # TODO: Add info about the results for the LLM
        content = json.dumps(
            {k: v for k, v in observation.items() if k not in ("results")}, indent=2
        )
        new_messages.append(
            ToolMessage(content=content, tool_call_id=agent_action.tool_call_id)
        )

        return new_messages