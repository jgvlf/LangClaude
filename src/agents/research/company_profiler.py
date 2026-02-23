from ..base import run_agent, AgentResult, parse_json_from_output


async def run_company_profiler(
    startup_name: str,
    startup_description: str
) -> AgentResult:
    prompt = f"""Research the following startup...
    
Format your response as valid JSON:
{{
    "name": "{startup_name}",
    "founded": "year or null",
    ...
}}
"""

    result = await run_agent(
        agent_name="company_profiler",
        prompt=prompt,
        tools=["WebSearch", "WebFetch"],
        model="haiku",
        timeout_seconds=90
    )

    if result.success and result.raw_output:
        parsed = parse_json_from_output(result.raw_output)
        if parsed:
            result.output = parsed

    return result