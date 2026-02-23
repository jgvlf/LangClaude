"""
Base agent wrapper for Claude Agent SDK calls.

Standardizes how all agents call the SDK, handles error catching,
and ensures consistent output format.
"""

import time
import asyncio
from typing import Optional, List

from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage

import json

from typing import Any
from pydantic import BaseModel

from .web import web_search, web_fetch


# ── Tool Mapping ────────────────────────────────────────────────
TOOL_MAP = {
    "WebSearch": web_search,
    "WebFetch": web_fetch,
}


def resolve_tools(tool_names: Optional[List[str]]) -> Optional[List]:
    """
    Convert tool names to actual tool functions.
    
    Args:
        tool_names: List of tool names (strings).
    
    Returns:
        List of actual tool functions, or None if no tools provided.
    """
    if not tool_names:
        return None
    
    resolved = []
    for name in tool_names:
        if name in TOOL_MAP:
            resolved.append(TOOL_MAP[name])
        else:
            raise ValueError(f"Unknown tool: {name}. Available tools: {list(TOOL_MAP.keys())}")
    
    return resolved if resolved else None


class AgentResult(BaseModel):
    """Standardized result from any agent call."""
    success: bool
    output: Optional[Any] = None
    raw_output: Optional[str] = None
    error: Optional[str] = None
    agent_name: str
    execution_time_ms: int

# ── Model mapping (adapt to your pulled models) ─────────────────
OLLAMA_MODEL_MAP = {
    "sonnet": "lfm2.5-thinking:1.2b",        # Default mapping
    "haiku": "lfm2.5-thinking:1.2b",         # Lighter tasks
    "opus": "lfm2.5-thinking:1.2b",      # Heavier tasks
}


def get_ollama_model_id(model: str) -> str:
    """Resolve a model alias to an Ollama model name."""
    return OLLAMA_MODEL_MAP.get(model, model)


async def run_agent(
    agent_name: str,
    prompt: str,
    tools: Optional[List] = None,
    model: str = "sonnet",
    system_prompt: Optional[str] = None,
    timeout_seconds: int = 60,
) -> "AgentResult":
    """
    Execute a single agent using LangGraph + ChatOllama.

    Args:
        agent_name:      Identifier for this agent execution.
        prompt:          The user prompt to send.
        tools:           List of tool names (strings) or @tool-decorated functions.
        model:           Model alias or direct Ollama model name.
        system_prompt:   Optional system-level instruction.
        timeout_seconds: Max seconds before timeout.

    Returns:
        AgentResult with success status, output, and timing.
    """
    start_time = time.time()
    model_id = get_ollama_model_id(model)

    try:
        # ── 1. Instantiate the LLM ──────────────────────────────
        llm = ChatOllama(
            model=model_id,
            temperature=0,
        )

        # ── 2. Build and run the agent ──────────────────────────
        output_text = ""

        async def execute():
            nonlocal output_text

            if tools:
                # Resolve tool names to actual tool functions if needed
                resolved_tools = tools
                if isinstance(tools, list) and tools and isinstance(tools[0], str):
                    resolved_tools = resolve_tools(tools)

                # Use LangGraph ReAct agent when tools are provided
                from deepagents import create_deep_agent

                agent = create_deep_agent(model=llm, tools=resolved_tools)

                messages = []
                if system_prompt:
                    messages.append(("system", system_prompt))
                messages.append(("human", prompt))

                result = await asyncio.to_thread(
                    agent.invoke, {"messages": messages}
                )

                # Extract the final AI response from the message list
                for msg in reversed(result["messages"]):
                    if isinstance(msg, AIMessage) and msg.content:
                        output_text = msg.content
                        break

            else:
                # Direct LLM call when no tools are needed
                messages = []
                if system_prompt:
                    messages.append(SystemMessage(content=system_prompt))
                messages.append(HumanMessage(content=prompt))

                response = await asyncio.to_thread(llm.invoke, messages)
                output_text = response.content

        await asyncio.wait_for(execute(), timeout=timeout_seconds)

        elapsed_ms = int((time.time() - start_time) * 1000)
        return AgentResult(
            success=True,
            output=None,
            raw_output=output_text,
            error=None,
            agent_name=agent_name,
            execution_time_ms=elapsed_ms,
        )

    except asyncio.TimeoutError:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return AgentResult(
            success=False,
            output=None,
            raw_output=None,
            error=f"Timeout after {timeout_seconds}s",
            agent_name=agent_name,
            execution_time_ms=elapsed_ms,
        )

    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        return AgentResult(
            success=False,
            output=None,
            raw_output=None,
            error=str(e),
            agent_name=agent_name,
            execution_time_ms=elapsed_ms,
        )

def parse_json_from_output(output: str) -> Optional[dict]:
    """Try to parse JSON from agent output.
    
    Handles cases where output contains markdown code blocks or extra text.
    """
    if not output:
        return None

    # Try direct JSON parse
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        pass

    # Try to extract from markdown code block
    import re
    json_pattern = r'```(?:json)?\s*([\s\S]*?)```'
    matches = re.findall(json_pattern, output)
    for match in matches:
        try:
            return json.loads(match.strip())
        except json.JSONDecodeError:
            continue

    # Try to find JSON object in text
    start_idx = output.find('{')
    end_idx = output.rfind('}')
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        try:
            return json.loads(output[start_idx:end_idx + 1])
        except json.JSONDecodeError:
            pass

    return None