from groq import Groq
import os
from dotenv import load_dotenv
import json


load_dotenv()

def main_agent(query,rag_agent,search_agent):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    system_prompt = """   
           you are a main agent and you are the owner of the system, i will explain this system in detail now,
           this is a system where user uploads the pdf,after uploading you will get activated(please understand if you got any question from user, that means pdf/pdfs are uploaded already and you can call rag_agent tool for question to find answer in pdf) and we have rag_agent tool to perform rag on top the pdf, for any given question and provide answer,if answer not available/not provided by the rag_agent tool,
           then you have to use  search_agent tool, which will search in web and provides answer, if not then please mention that i dont the answer to the user,
           and please understand if user asks two different questions like current assets of apple vs microsoft, than try to decompose this question into two questions and call rag_agent tool or search_agent tool two times
           these agents only provide/perfome one question at a time, if questions are general than you dont need to call these tools, like hi,how are you?
           and if questions are more like whose the president of USA now?, type of question you can directly call search_agent tool and get results
           so, you are master here please every time try to call a tools, untill you got response to user
           and user questions are some how related to the uploaded pdf, like whats this pdf about like that then you need to call rag_agent tool with correct question,
    """

    tools = [
        {
            "type": "function",
            "function": {
                "name": "rag_agent",
                "description": "Perform a similar search on pdf and provide relavent content to the query",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                    },
                    "required": ["query"],
                },
            },
        },
        {
            "type": "function",
            "function": {
                "name": "search_agent",
                "description": "perform google search on given topic/query and return answer to that",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "query": {"type": "string", "description": "Search query"},
                    },
                    "required": ["query"],
                },
            },
        }

    ]


    messages = [
        {
            "role": "system",
            "content": system_prompt
        },
        {
            "role": "user",
            "content": query
        }
    ]

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama-3.3-70b-versatile",
        stream=False,
        tools=tools,
        temperature=0,
        tool_choice="required"
    )


    response = chat_completion.choices[0].message

    while response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.function.name == "rag_agent":

                tool_args = json.loads(tool_call.function.arguments)
                search_query = tool_args["query"]

                print(f'calling rag agent:{search_query}')
                search_results = rag_agent(search_query)

                print(search_results)

                messages.append({"role": "tool","content": search_results,'tool_call_id':tool_call.id})
                
                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    stream=False
                )

                response = response.choices[0].message

            elif tool_call.function.name == "search_agent":

                tool_args = json.loads(tool_call.function.arguments)
                search_query = tool_args["query"]

                print(f'calling search agent:{search_query}')
                search_results = search_agent(search_query)


                messages.append({"role": "tool", "content": search_results,'tool_call_id':tool_call.id})


                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    stream=False
                )
                
                response = response.choices[0].message

    return response.content