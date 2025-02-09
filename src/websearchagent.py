from duckduckgo_search import DDGS
from groq import Groq
import os
from dotenv import load_dotenv
import json

load_dotenv()

def web_search(query):
    results = DDGS().text(query, max_results=5)
    return results


def search_agent(query):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )


    tools = [
        {
            "type": "function",
            "function": {
                "name": "web_search",
                "description": "Perform a web search using DuckDuckGo.",
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
            "content": "Your name is Siva, you are a chatbot with web search capabilities. If the user asks for recent information, use the web search tool."
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
            if tool_call.function.name == "web_search":

                tool_args = json.loads(tool_call.function.arguments)
                search_query = tool_args["query"]

                search_results = web_search(search_query)


                messages.append({"role": "assistant", "content": f"Here are the search results:\n{search_results}"})


                response = client.chat.completions.create(
                    messages=messages,
                    model="llama-3.3-70b-versatile",
                    stream=False
                )

                response = response.choices[0].message
                # print(response.choices[0].message.content)

    return response.content