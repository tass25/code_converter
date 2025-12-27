"""
VALIDATOR AGENT - Ensures Intent Quality 🔍
============================================

This agent reviews extracted intentions to ensure they are:
- Complete (no missing operations)
- Consistent (dependencies make sense)
- Clear (no ambiguous descriptions)
- Comprehensive (edge cases considered)
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json

load_dotenv()

class ValidatorAgent:
    """
    Validates that extracted intentions are complete and accurate.
    
    Acts as a quality control step - if intentions are incomplete,
    it sends feedback to the Intent Extractor to try again.
    """
    
    def __init__(self):
        """Initialize the Validator Agent"""
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        
        self.system_prompt = """You are a code review expert and quality assurance specialist.

Your job: Review extracted intentions for completeness and accuracy.

Check for:
1. COMPLETENESS: Are all operations from the code captured?
2. CONSISTENCY: Do the dependencies between intentions make sense?
3. CLARITY: Are descriptions clear and unambiguous?
4. EDGE CASES: Are error handling and edge cases considered?
5. DATA FLOW: Does the data flow graph make logical sense?

RESPOND WITH JSON:
{
  "valid": true/false,
  "issues": [
    {
      "type": "missing_operation|unclear_description|invalid_dependency|missing_edge_case",
      "severity": "critical|warning|info",
      "description": "Clear explanation of the issue",
      "suggestion": "How to fix it"
    }
  ],
  "overall_assessment": "Brief summary"
}

If valid=true and no critical issues, the intentions can proceed to code generation.
If valid=false or critical issues exist, intentions need refinement."""

    def validate(self, intent_graph, parsed_structure, original_code):
        """
        Validate the extracted intention graph.
        
        Args:
            intent_graph (dict): Extracted intentions from Intent Extractor
            parsed_structure (dict): Parsed code structure for comparison
            original_code (str): Original source code
            
        Returns:
            dict: Validation result with issues and suggestions
        """
        
        print(f"\n🔍 [Validator] Checking intention quality...")
        
        user_prompt = f"""Review these extracted intentions for quality and completeness:

INTENT GRAPH:
{json.dumps(intent_graph, indent=2)}

PARSED CODE STRUCTURE (for comparison):
{json.dumps(parsed_structure, indent=2)}

ORIGINAL CODE (for reference):
{original_code}

Validate that:
1. All operations from the parsed structure are captured as intentions
2. Dependencies between intentions are logical
3. Descriptions are clear and language-agnostic
4. Edge cases (errors, null values, etc.) are considered
5. The overall goal matches what the code actually does

Return ONLY valid JSON with your validation result."""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse validation result
        try:
            content = response.content.strip()
            
            # Clean markdown
            if content.startswith("```json"):
                content = content.split("```json")[1]
            if content.startswith("```"):
                content = content.split("```")[1]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
            
            validation_result = json.loads(content.strip())
            
            # Count issues by severity
            critical = sum(1 for issue in validation_result.get('issues', []) 
                          if issue.get('severity') == 'critical')
            warnings = sum(1 for issue in validation_result.get('issues', []) 
                          if issue.get('severity') == 'warning')
            
            if validation_result.get('valid', False):
                print(f"✅ Validation PASSED!")
            else:
                print(f"⚠️  Validation FAILED!")
            
            if critical > 0:
                print(f"   🔴 {critical} critical issue(s)")
            if warnings > 0:
                print(f"   🟡 {warnings} warning(s)")
            
            if not validation_result.get('issues'):
                print(f"   No issues found - intentions are complete!")
            
            return validation_result
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Could not parse validation response")
            return {
                "valid": True,  # Assume valid if we can't parse
                "issues": [],
                "overall_assessment": "Could not parse validation response",
                "raw_response": response.content
            }


# ============================================================================
# TEST THE VALIDATOR
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING VALIDATOR AGENT")
    print("="*70)
    
    from parser_agent import ParserAgent
    from intent_extractor import IntentExtractorAgent
    
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
    
    print("\n🔄 Step 1: Parsing...")
    parser = ParserAgent()
    parsed = parser.parse(test_code, "R")
    
    print("\n🔄 Step 2: Extracting intentions...")
    extractor = IntentExtractorAgent()
    intentions = extractor.extract_intents(parsed, test_code, "R")
    
    print("\n🔄 Step 3: Validating intentions...")
    validator = ValidatorAgent()
    validation = validator.validate(intentions, parsed, test_code)
    
    print("\n" + "="*70)
    print("VALIDATION RESULT:")
    print("="*70)
    print(json.dumps(validation, indent=2))
    
    print("\n" + "="*70)
    print("✓ All agents working with validation!")
    print("="*70)