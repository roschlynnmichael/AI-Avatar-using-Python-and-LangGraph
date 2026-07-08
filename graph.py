import os
from pydoc import text
import re
from dotenv import load_dotenv
from typing import TypedDict, Annotated, List, Sequence
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

load_dotenv(".env")

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], "Conversation history"]
    mood: str
    avatar_animation: str
    final_text: str

llm = ChatOpenAI(
    model="llama3.2:3b",
    openai_api_base="http://localhost:11434/v1",
    openai_api_key="ollama",
    temperature=0.7
)

def clean_text(text: str) -> str:
    return re.sub(r'\[.*?\]', '', text).strip()

def trim_history(state: AgentState):
    messages = state["messages"]
    if len(messages) > 6:
        return {"messages": messages[-6:]}
    return {"messages": messages}

def think_node(state: AgentState):
    system_prompt = SystemMessage(content = (
        "You are Kai, a curious, friendly 20 year old."
        "Your responses are natural, empathetic and engaging."
        "After your text response, provide a mood descriptor in brackets like [happy], [curious] or [thoughtful]."
    ))
    messages = [system_prompt] + state["messages"]
    response = llm.invoke(messages)
    raw_text = response.content
    mood = 'neutral'
    if "[happy]" in raw_text:
        mood = 'happy'
    elif "[curious]" in raw_text:
        mood = 'curious'
    elif "[thoughtful]" in raw_text: mood = "thoughtful"
    anim_map = {
        "happy": "talk_excited", 
        "curious": "talk_thinking", 
        "thoughtful": "talk_thoughtful",
        "neutral": "talk_standard"
    }
    return {
        "messages": [AIMessage(content=raw_text)],
        "mood": mood,
        "avatar_animation": anim_map.get(mood, "talk_standard"),
        "final_text": clean_text(raw_text)
    }

workflow = StateGraph(AgentState)

workflow.add_node("trimmer", trim_history)
workflow.add_node("think", think_node)

workflow.set_entry_point("trimmer")
workflow.add_edge("trimmer", "think")
workflow.add_edge("think", END)

app = workflow.compile()