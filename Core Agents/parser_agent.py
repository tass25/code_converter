"""
PARSER AGENT - Step 1 of our Code Converter
==========================================

This agent analyzes source code and extracts structural information.

What it does:
1. Takes code as input (e.g., R code)
2. Asks the LLM to understand the code structure
3. Returns structured information about variables, operations, libraries, etc.

This is the FIRST agent in our pipeline.
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json

# Load environment variables
load_dotenv()

class ParserAgent:
    """
    The Parser Agent understands code structure.
    
    Think of it as a code detective - it looks at code and figures out:
    - What variables are being used
    - What operations are being performed
    - What libraries are needed
    - What the code is trying to do
    """
    
    def __init__(self):
        """Initialize the agent with Groq LLM"""
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0  # 0 = deterministic (same input = same output)
        )
        
        # This is the agent's "personality" and instructions
        self.system_prompt = """You are a code structure analyzer.

Your job is to analyze code and extract structural information.

When given code, extract:
1. Variables and their purposes
2. Data structures being used (dataframes, lists, arrays, etc.)
3. Operations performed (transformations, calculations, etc.)
4. Libraries/packages being used
5. Control flow (if statements, loops, etc.)
6. Inputs (data sources like files, databases)
7. Outputs (what the code produces)

IMPORTANT: Respond ONLY with valid JSON. No explanations before or after.

Output format:
{
  "variables": ["list of variable names"],
  "data_structures": ["types of data structures"],
  "operations": [
    {"type": "operation_type", "details": "description"}
  ],
  "libraries": ["library1", "library2"],
  "control_flow": ["description of if/for/while statements"],
  "inputs": ["data sources"],
  "outputs": ["what is produced"]
}"""
    
    def parse(self, source_code, language):
        """
        Parse the source code and extract structure.
        
        Args:
            source_code (str): The code to analyze
            language (str): Programming language (e.g., "R", "Python")
            
        Returns:
            dict: Structured information about the code
        """
        
        print(f"\n🔍 [Parser Agent] Analyzing {language} code...")
        
        # Create the prompt for the LLM
        user_prompt = f"""Analyze this {language} code:

```{language}
{source_code}
```

Extract the structural information as JSON."""

        # Send to LLM
        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse the JSON response
        try:
            # Clean up response (remove markdown if present)
            content = response.content.strip()
            if content.startswith("```json"):
                content = content.split("```json")[1]
            if content.startswith("```"):
                content = content.split("```")[1]
            if content.endswith("```"):
                content = content.rsplit("```", 1)[0]
            
            parsed_info = json.loads(content.strip())
            
            print(f"✅ Parsed successfully!")
            print(f"   Found {len(parsed_info.get('variables', []))} variables")
            print(f"   Found {len(parsed_info.get('operations', []))} operations")
            print(f"   Found {len(parsed_info.get('libraries', []))} libraries")
            
            return parsed_info
            
        except json.JSONDecodeError as e:
            print(f"⚠️  Warning: Could not parse JSON response")
            print(f"   Raw response: {response.content[:200]}...")
            
            # Return a fallback structure
            return {
                "raw_analysis": response.content,
                "parsing_status": "failed_json_parse",
                "error": str(e)
            }


# ============================================================================
# TEST THE PARSER AGENT
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TESTING PARSER AGENT")
    print("="*70)
    
    # Create the agent
    parser = ParserAgent()
    
    # Test with a simple R code example
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
    
    # Parse the code
    result = parser.parse(test_code, "R")
    
    # Show results
    print("\n" + "="*70)
    print("PARSER RESULTS:")
    print("="*70)
    print(json.dumps(result, indent=2))