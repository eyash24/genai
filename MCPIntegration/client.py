from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain.chat_models import init_chat_model

from dotenv import load_dotenv
load_dotenv()

import asyncio


async def main():
    client = MultiServerMCPClient(
        {
            'math':{
                "command": 'python',
                'args': ['/Users/eyash.p24/Code/GenAI/MCPIntegration/mathserver.py'],
                'transport': 'stdio',
            },
            'weather':{
                'url': 'http://localhost:8000/mcp',
                'transport': 'streamable_http'
            }
              
        }
    )

    import os
    os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')

    tools = await client.get_tools()

    # model = ChatGroq(model='qwen3-32b')
    model = init_chat_model(model='groq:qwen/qwen3-32b')
    agent = create_agent(
        model, tools
    )

    math_response = await agent.ainvoke({
        'messages': [{'role':'user', 'content':'what is (7+9)x3?'}]
    })

    print('Math response: ', math_response['messages'][-1].content)

    weather_reponse = await agent.ainvoke({
        'messages':[{'role':'user', 'content':'what is the weather of Bangalore?'}]
    })

    print('weather resposne: ', weather_reponse['messages'][-1].content)


asyncio.run(main())
     