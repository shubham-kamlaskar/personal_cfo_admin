import os
import uuid
from dotenv import load_dotenv
import logging
from langchain.agents import create_agent

from src.AI.llm.llm_provider import LLMProvider
from src.prompt.prompt_provider import Prompt
from src.tools.tool_provider import CreateTestCase

load_dotenv()

logger = logging.getLogger(__name__)
llm_provider = LLMProvider()
tools = [CreateTestCase]

    
def get_agent_client():
    try:      
        agent = create_agent(
                model=llm_provider.llm_client(),
                tools=tools,
                system_prompt=(Prompt.DEFAULT_SYSTEM_PROMPT + Prompt.VALIDATION_PROMPT + Prompt.OUT_OF_SCOPE_PROMPT),
                debug=True,
            )
        return agent
    except Exception as e:
        logger.exception(f"An error occured in get_agent_client call {str(e)}")
        raise Exception(f"An error occured in get_agent_client call {str(e)}")

def get_agent_response(user_query: str):
    try:
        answer = None
        agent_client = get_agent_client()
            
        response = agent_client.invoke(
            {
                "messages": [{"role": "user", "content": user_query}],
            },
        )
        if response:
            messages = response.get("messages", [])

            response_call = messages[-1] if messages else None              

            answer = response_call.content
        else:
            answer =  "Failed to generate any response."
            
        return answer   

    except Exception as e:
        logger.exception(f"An error occured in get_agent_response call {str(e)}")
        raise Exception(f"An error occured in get_agent_response call {str(e)}")
    
def test_case_creation(requirement):
    llm_client = llm_provider.llm_client()
    test_case = llm_client.invoke(requirement)
    file_name = str(uuid.uuid4())
    file_path = os.path.join("output", "test_cases", f"{file_name}.txt")
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(f"{test_case}")
    return {"test_case": test_case}
    
if __name__ == "__main__":
    answer = test_case_creation(requirement=input("Query: "))
    print(answer)
    