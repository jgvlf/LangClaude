"""Type-safe enums for state field names and workflow stages.

Using enums instead of raw strings prevents typos and enables IDE autocomplete.
"""

from enum import Enum


class StateField(str, Enum):
    """Field names for DueDiligenceState.

    Use these instead of raw strings to prevent typos:
        state[StateField.STARTUP_NAME]  # IDE catches typos
        state["startup_name"]            # Typos silently fail
    """
    STARTUP_NAME = "startup_name"
    STARTUP_DESCRIPTION = "startup_description"
    FUNDING_STAGE = "funding_stage"
    RESEARCH_OUTPUTS = "research_outputs"
    ANALYSIS_OUTPUTS = "analysis_outputs"
    FULL_REPORT = "full_report"
    INVESTMENT_DECISION = "investment_decision"
    CURRENT_STAGE = "current_stage"
    ERRORS = "errors"
    RETRY_COUNT = "retry_count"


class Stage(str, Enum):
    """Workflow stages for tracking progress.

    Use in routing functions and node returns:
        return {StateField.CURRENT_STAGE: Stage.RESEARCH_COMPLETE}
    """
    INIT = "init"
    INIT_COMPLETE = "init_complete"
    RESEARCH_COMPLETE = "research_complete"
    RESEARCH_VALIDATED = "research_validated"
    ANALYSIS_COMPLETE = "analysis_complete"
    SYNTHESIS_COMPLETE = "synthesis_complete"
    COMPLETE = "complete"
    PARTIAL = "partial"
    FAILED = "failed"


class AgentName(str, Enum):
    """Agent identifiers for configuration and logging.

    Matches names in agent_configs.py:
        COMPANY_PROFILER.name == AgentName.COMPANY_PROFILER.value
    """
    # Research agents (Layer 1)
    COMPANY_PROFILER = "company_profiler"
    MARKET_RESEARCHER = "market_researcher"
    COMPETITOR_SCOUT = "competitor_scout"
    TEAM_INVESTIGATOR = "team_investigator"
    NEWS_MONITOR = "news_monitor"

    # Analysis agents (Layer 2)
    FINANCIAL_ANALYST = "financial_analyst"
    RISK_ASSESSOR = "risk_assessor"
    TECH_EVALUATOR = "tech_evaluator"
    LEGAL_REVIEWER = "legal_reviewer"

    # Synthesis agents (Layer 3)
    REPORT_GENERATOR = "report_generator"
    DECISION_AGENT = "decision_agent"