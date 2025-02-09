from groq import Groq
import os
from dotenv import load_dotenv
import json

def rag_agent(query,retrieve_chunks):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )


    tools = [
        {
            "type": "function",
            "function": {
                "name": "retrieve_chunks",
                "description": "Perform a similar search on pdf and provide relavent content to the query",
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
            "content": "your a bot, whose job is to answer given question using retrive_chunks tool"
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

    if response.tool_calls:
        for tool_call in response.tool_calls:
            if tool_call.function.name == "retrieve_chunks":

                tool_args = json.loads(tool_call.function.arguments)
                search_query = tool_args["query"]

                search_results = retrieve_chunks(search_query)


                messages.append({"role": "assistant", "content": f"Here are the search results:\n{search_results}"})


                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    stream=False
                )

                response = response.choices[0].message
                # print(final_response.choices[0].message.content)
    else:
        # print(response.content)
        pass

    return response.content