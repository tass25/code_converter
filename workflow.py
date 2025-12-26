# ============================================================================ 
# LANGGRAPH WORKFLOW - Complete Agent Orchestration 🔄
# ============================================================================

"""
This connects all agents together with proper state management
and feedback loops for quality control.

Flow:
1. Parser → 2. Intent Extractor → 3. Validator
   ↓ (if invalid)                      ↓ (if valid)
   ← Feedback loop ←                   4. Generator → Output
"""

import os
import time
from typing import TypedDict
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

from parser_agent import ParserAgent
from intent_extractor import IntentExtractorAgent
from validator_agent import ValidatorAgent
from code_generator import CodeGeneratorAgent

from elasticsearch_logger import get_logger

load_dotenv()

# ============================================================================ 
# STATE DEFINITION
# ============================================================================ 

class ConversionState(TypedDict):
    """
    State passed between agents.
    
    This is like a shared notebook that all agents can read and write to.
    """
    # Input
    source_code: str
    source_language: str
    target_language: str
    
    # Agent outputs
    parsed_structure: dict
    intent_graph: dict
    validation_result: dict
    generated_code: str
    
    # Metadata
    iteration_count: int
    max_iterations: int
    status: str
    error_message: str


# ============================================================================ 
# AGENT NODE FUNCTIONS
# ============================================================================ 

def parse_node(state: ConversionState) -> ConversionState:
    """Node 1: Parse source code"""
    print("\n" + "="*70)
    print("NODE 1: PARSER")
    print("="*70)
    
    parser = ParserAgent()
    parsed = parser.parse(state["source_code"], state["source_language"])
    
    state["parsed_structure"] = parsed
    return state


def extract_intents_node(state: ConversionState) -> ConversionState:
    """Node 2: Extract intentions"""
    print("\n" + "="*70)
    print("NODE 2: INTENT EXTRACTOR")
    print("="*70)
    
    extractor = IntentExtractorAgent()
    intentions = extractor.extract_intents(
        state["parsed_structure"],
        state["source_code"],
        state["source_language"]
    )
    
    state["intent_graph"] = intentions
    state["iteration_count"] = state.get("iteration_count", 0) + 1
    return state


def validate_node(state: ConversionState) -> ConversionState:
    """Node 3: Validate intentions"""
    print("\n" + "="*70)
    print("NODE 3: VALIDATOR")
    print("="*70)
    
    validator = ValidatorAgent()
    validation = validator.validate(
        state["intent_graph"],
        state["parsed_structure"],
        state["source_code"]
    )
    
    state["validation_result"] = validation
    return state


def generate_node(state: ConversionState) -> ConversionState:
    """Node 4: Generate target code"""
    print("\n" + "="*70)
    print("NODE 4: CODE GENERATOR")
    print("="*70)
    
    generator = CodeGeneratorAgent(target_language=state["target_language"])
    generated = generator.generate(
        state["intent_graph"],
        state["source_code"],
        state["source_language"]
    )
    
    state["generated_code"] = generated
    state["status"] = "success"
    return state


# ============================================================================ 
# CONDITIONAL ROUTING
# ============================================================================ 

def should_retry(state: ConversionState) -> str:
    """
    Decide if we should retry intent extraction or proceed to generation.
    
    Returns:
        "extract_intents" if validation failed and we haven't hit max iterations
        "generate" if validation passed or we've hit max iterations
    """
    
    validation = state.get("validation_result", {})
    is_valid = validation.get("valid", False)
    iteration = state.get("iteration_count", 0)
    max_iter = state.get("max_iterations", 3)
    
    # Check for critical issues
    critical_issues = [
        issue for issue in validation.get("issues", [])
        if issue.get("severity") == "critical"
    ]
    
    if not is_valid or critical_issues:
        if iteration < max_iter:
            print(f"\n⚠️  Validation failed. Retrying ({iteration}/{max_iter})...")
            return "extract_intents"
        else:
            print(f"\n⚠️  Max iterations reached. Proceeding anyway...")
            return "generate"
    else:
        print(f"\n✅ Validation passed. Proceeding to generation...")
        return "generate"


# ============================================================================ 
# BUILD THE WORKFLOW
# ============================================================================ 

def create_workflow():
    """
    Create the LangGraph workflow with all agents and feedback loops.
    """
    
    # Initialize graph
    workflow = StateGraph(ConversionState)
    
    # Add nodes (agents)
    workflow.add_node("parse", parse_node)
    workflow.add_node("extract_intents", extract_intents_node)
    workflow.add_node("validate", validate_node)
    workflow.add_node("generate", generate_node)
    
    # Add edges (connections)
    workflow.add_edge("parse", "extract_intents")
    workflow.add_edge("extract_intents", "validate")
    
    # Conditional edge: retry or proceed
    workflow.add_conditional_edges(
        "validate",
        should_retry,
        {
            "extract_intents": "extract_intents",  # Loop back
            "generate": "generate"  # Proceed forward
        }
    )
    
    # End after generation
    workflow.add_edge("generate", END)
    
    # Set entry point
    workflow.set_entry_point("parse")
    
    # Compile
    return workflow.compile()


# ============================================================================ 
# MAIN CONVERSION FUNCTION WITH ELASTICSEARCH LOGGING
# ============================================================================ 

def convert_with_workflow(source_code, source_lang="R", target_lang="Python", max_iterations=3):
    """
    Convert code using the complete LangGraph workflow with Elasticsearch logging.
    
    Args:
        source_code (str): Source code to convert
        source_lang (str): Source programming language
        target_lang (str): Target programming language
        max_iterations (int): Max retry attempts for intent extraction
        
    Returns:
        dict: Final state with generated code
    """
    
    logger = get_logger()
    start_time = time.time()
    
    print("="*70)
    print(f"🚀 STARTING WORKFLOW: {source_lang} → {target_lang}")
    print("="*70)
    
    # Initialize state
    initial_state = ConversionState(
        source_code=source_code,
        source_language=source_lang,
        target_language=target_lang,
        parsed_structure={},
        intent_graph={},
        validation_result={},
        generated_code="",
        iteration_count=0,
        max_iterations=max_iterations,
        status="in_progress",
        error_message=""
    )
    
    # Create and run workflow
    app = create_workflow()
    
    try:
        final_state = app.invoke(initial_state)
        duration = time.time() - start_time
        
        # Log successful conversion
        logger.log_conversion(
            source_lang=source_lang,
            target_lang=target_lang,
            status="success",
            duration=duration,
            iterations=final_state.get('iteration_count', 0),
            code_length=len(final_state.get('generated_code', '')),
            metadata={
                "intent_count": len(final_state.get('intent_graph', {}).get('intents', [])),
                "validation_passed": final_state.get('validation_result', {}).get('valid', False)
            }
        )
        
        print("\n" + "="*70)
        print("✅ WORKFLOW COMPLETE!")
        print("="*70)
        print(f"Status: {final_state.get('status', 'unknown')}")
        print(f"Iterations: {final_state.get('iteration_count', 0)}")
        print(f"Generated: {len(final_state.get('generated_code', ''))} characters")
        
        return final_state
        
    except Exception as e:
        duration = time.time() - start_time
        
        # Log failed conversion
        logger.log_conversion(
            source_lang=source_lang,
            target_lang=target_lang,
            status="failed",
            duration=duration
        )
        
        logger.log_error(
            error_type="workflow_error",
            message=str(e),
            context={"source_lang": source_lang, "target_lang": target_lang}
        )
        
        print(f"\n❌ ERROR in workflow: {e}")
        import traceback
        traceback.print_exc()
        return None


# ============================================================================ 
# TEST THE COMPLETE WORKFLOW
# ============================================================================ 

if __name__ == "__main__":
    test_code = """
library(dplyr)

data <- read.csv("data.csv")

result <- data %>%
  filter(age > 18) %>%
  group_by(category) %>%
  summarise(
    total = sum(amount),
    average = mean(amount),
    count = n()
  ) %>%
  arrange(desc(total))

write.csv(result, "output.csv")
print(result)
"""
    
    print("TESTING COMPLETE LANGGRAPH WORKFLOW")
    print("="*70)
    
    result = convert_with_workflow(test_code, "R", "Python")
    
    if result:
        print("\n" + "="*70)
        print("FINAL GENERATED CODE:")
        print("="*70)
        print(result["generated_code"])
        print("="*70)
        
        # Save to file
        with open("workflow_output.py", "w") as f:
            f.write(result["generated_code"])
        print("\n✅ Saved to workflow_output.py")
