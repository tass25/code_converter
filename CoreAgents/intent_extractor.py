"""
INTENT EXTRACTOR AGENT - The Core Innovation! 🧠
================================================

This agent extracts HIGH-LEVEL developer intentions from code.

This is THE KEY innovation that makes our system different:
- Traditional: "dplyr::group_by()" → "pandas.groupby()"
- Our approach: "dplyr::group_by()" → "Group data by category" → "pandas.groupby()"

The intent is language-agnostic - it can generate code in ANY language!
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json

load_dotenv()

class IntentExtractorAgent:
    """
    Extracts developer intentions from parsed code structure.
    
    This agent thinks about WHAT the developer wanted to do,
    not HOW they did it in the source language.
    """
    
    def __init__(self):
        """Initialize the Intent Extractor with Groq LLM"""
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        
        self.system_prompt = """You are an expert at understanding developer intent.

Your job: Extract HIGH-LEVEL intentions from code, NOT syntax details.

Key principle: Think about WHAT the developer wanted to achieve, not HOW they coded it.

Example of GOOD intent extraction:
❌ BAD: "Call dplyr::group_by() then summarise()"
✅ GOOD: "Group data by categorical column, then compute aggregate statistics"

Each intention should be:
- Language-agnostic (no mention of specific functions/syntax)
- Focused on WHAT, not HOW
- Clear and descriptive

IMPORTANT: Respond ONLY with valid JSON. No explanations.

Output format:
{
  "intents": [
    {
      "id": "intent_1",
      "type": "data_loading|transformation|aggregation|visualization|filtering|etc",
      "description": "Clear description of what developer wants to achieve",
      "parameters": {
        "param_name": "param_value"
      },
      "depends_on": []
    }
  ],
  "data_flow": {
    "intent_1": ["intent_2"],
    "intent_2": ["intent_3"]
  },
  "overall_goal": "One sentence: what does this code accomplish?"
}"""
    
    def extract_intents(self, parsed_code, original_code, source_language):
        """
        Extract developer intentions from parsed code structure.
        
        Args:
            parsed_code (dict): Output from Parser Agent
            original_code (str): The original source code
            source_language (str): Source programming language
            
        Returns:
            dict: Intent graph with high-level intentions
        """
        
        print(f"\n🧠 [Intent Extractor] Extracting developer intentions...")
        
        user_prompt = f"""Based on this code analysis, extract the HIGH-LEVEL intentions:

Source Language: {source_language}

Parsed Code Structure:
{json.dumps(parsed_code, indent=2)}

Original Code:
```{source_language}
{original_code}
```

Remember: Extract WHAT the developer wanted to do, not the specific syntax they used.
Make intentions language-agnostic so they can be implemented in any programming language.

Return ONLY valid JSON with the intent graph."""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse JSON response
        try:
            content = response.content.strip()
            
            # Clean markdown formatting if present
            if content.startswith("```json"):
                content = content.split("```json")[1]
            if content.startswith("```"):
                content = content.split("```")[1]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
            
            intent_graph = json.loads(content.strip())
            
            print(f"✅ Extracted {len(intent_graph.get('intents', []))} intentions")
            print(f"   Overall goal: {intent_graph.get('overall_goal', 'N/A')}")
            
            # Show each intention
            for intent in intent_graph.get('intents', []):
                print(f"   • {intent['id']}: {intent['description']}")
            
            return intent_graph
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Could not parse JSON response")
            print(f"   Raw response: {response.content[:200]}...")
            
            return {
                "raw_intents": response.content,
                "parsing_status": "failed_json_parse",
                "error": str(e)
            }


# ============================================================================
# TEST THE INTENT EXTRACTOR
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING INTENT EXTRACTOR AGENT")
    print("="*70)
    
    # Import Parser Agent
    from parser_agent import ParserAgent
    
    # Test code
    test_code = """
library(dplyr)

# Load sales data
sales_data <- read.csv("sales.csv")

# Calculate average sales by country
country_avg <- sales_data %>%
  group_by(country) %>%
  summarise(avg_sales = mean(sales))

print(country_avg)
"""
    
    # Step 1: Parse the code
    print("\nStep 1: Parsing code structure...")
    parser = ParserAgent()
    parsed_result = parser.parse(test_code, "R")
    
    # Step 2: Extract intentions
    print("\nStep 2: Extracting intentions...")
    extractor = IntentExtractorAgent()
    intent_graph = extractor.extract_intents(parsed_result, test_code, "R")
    
    # Show final result
    print("\n" + "="*70)
    print("INTENT GRAPH:")
    print("="*70)
    print(json.dumps(intent_graph, indent=2))
    
    print("\n" + "="*70)
    print("🎉 TWO AGENTS WORKING TOGETHER!")
    print("="*70)
    print("✓ Parser Agent analyzed the code structure")
    print("✓ Intent Extractor understood what the developer wanted")
