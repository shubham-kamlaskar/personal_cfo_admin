import uuid
import os
from langchain.tools import tool
from src.tools.tool_pydantic_provider import CreateTestCase
from src.AI.llm.llm_provider import LLMProvider

llm_provider = LLMProvider()

def test_case_creation(requirement):
    llm_client = llm_provider.llm_client()
    test_case = llm_client.invoke(requirement)
    file_name = str(uuid.uuid4())
    file_path = os.path.join("output", "test_cases", f"{file_name}.txt")
    with open(file_path, "w") as file:
        file.write(f"{test_case}")
    return {"test_case": test_case}

@tool('create_test_case', args_schema=CreateTestCase)
def create_test_case(requirement: str):
    "Create test cases based on the provided business and technical requirements and store it in pre-defined folder."
    return  test_case_creation(requirement)
    