from typing import Annotated
from typing_extensions import TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage
from langchain.chat_models import init_chat_model

import os
from dotenv import load_dotenv

load_dotenv()

os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
os.environ['LANGSMITH_API_KEY'] = os.getenv('LANGSMITH_API_KEY')
os.environ['LANGSMITH_TRACING'] = 'true'
os.environ['LANGSMITH_PROJECT'] = 'SmithTut'

llm = init_chat_model('groq:llama-3.1-8b-instant')

class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def make_tool_graph():
    # graph with tool call

    @tool
    def multiply(a:float, b:float)->float:
        """Multiply two numbers"""
        return a*b
    
    tools = [multiply]
    
    llm_with_tool = llm.bind_tools(tools)

    def call_llm_model(state:State):
        return {'messages':[llm_with_tool.invoke(state['messages'])]}
    
    # nodes
    builder = StateGraph(State)
    builder.add_node('tool_calling_llm', call_llm_model)
    builder.add_node('tools', ToolNode(tools))

    # edges
    builder.add_edge(START, 'tool_calling_llm')
    builder.add_conditional_edges(
        'tool_calling_llm',
        tools_condition
    )
    builder.add_edge('tools', 'tool_calling_llm')

    # compile
    graph = builder.compile()
    return graph


tool_agent = make_tool_graph()




    