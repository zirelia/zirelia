# Copyright (c) 2026 Antonio Trento (antoniotrento.net)
# Project: Zirelia - AI Virtual Influencer Engine
# License: Elastic License 2.0 (ELv2) - https://www.elastic.co/licensing/elastic-license

from typing import Dict, TypedDict, Annotated, List
import operator
from langgraph.graph import StateGraph, END
from core.persona.brain import PersonaBrain
from core.safety.manager import SafetyManager
from core.utils.logger import logger

# Define State
class AgentState(TypedDict):
    platform: str
    context: str
    draft: str
    image_prompt: str
    critique: str
    revision_count: int
    is_safe: bool

class ContentWorkflow:
    def __init__(self):
        self.brain = PersonaBrain()
        self.safety = SafetyManager()
        self.workflow = self._build_graph()

    def _build_graph(self):
        # 1. Define Nodes
        def draft_node(state: AgentState):
            logger.info(f"Drafting content for {state['platform']}...")
            draft = self.brain.generate_thought(state['context'], state['platform'])
            return {"draft": draft, "revision_count": state.get("revision_count", 0) + 1}

        def critique_node(state: AgentState):
            logger.info("Critiquing content...")
            draft = state['draft']
            
            # 1. Safety Check (Hard)
            if not self.safety.validate_content(draft):
                return {"is_safe": False, "critique": "Content contains prohibited keywords."}
            
            # 2. Persona Check (Mock LLM critique)
            # In a real system, another LLM call would check if it sounds like the persona.
            return {"is_safe": True, "critique": "Looks good."}

        # 2. Build Graph
        workflow = StateGraph(AgentState)
        
        workflow.add_node("drafter", draft_node)
        workflow.add_node("critic", critique_node)
        
        # 3. Define Edges
        workflow.set_entry_point("drafter")
        workflow.add_edge("drafter", "critic")
        
        def check_safety(state: AgentState):
            if state['is_safe']:
                return "end"
            if state['revision_count'] > 3:
                logger.warning("Max revisions reached. Ending.")
                return "end"
            return "retry"

        workflow.add_conditional_edges(
            "critic",
            check_safety,
            {
                "end": END,
                "retry": "drafter"
            }
        )
        
        return workflow.compile()

    def run(self, platform: str, context: str):
        """Runs the content generation workflow."""
        inputs = {"platform": platform, "context": context, "revision_count": 0}
        result = self.workflow.invoke(inputs)
        return result
