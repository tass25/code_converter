"""
CODE GENERATOR AGENT - Creates Idiomatic Target Code 💻
========================================================

This agent takes language-agnostic intentions and generates
clean, idiomatic code in the target language.

Key principle: Write code as a NATIVE developer would,
not as a literal translation!
"""

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import json

load_dotenv()

class CodeGeneratorAgent:
    """
    Generates idiomatic code in the target language from intentions.
    
    This agent knows best practices for each language and writes
    code the way an expert developer would.
    """
    
    def __init__(self, target_language="Python"):
        """
        Initialize the Code Generator.
        
        Args:
            target_language (str): Target programming language (default: Python)
        """
        self.target_language = target_language
        self.llm = ChatGroq(
            api_key=os.getenv("GROQ_API_KEY"),
            model="llama-3.3-70b-versatile",
            temperature=0
        )
        
        # Language-specific best practices
        self.language_profiles = {
            "Python": {
                "data_loading": "Use pandas.read_csv() for CSV files",
                "grouping": "Use DataFrame.groupby() for grouping operations",
                "aggregation": "Use .agg() or specific methods like .mean(), .sum()",
                "output": "Use print() or return for displaying results",
                "best_practices": [
                    "Use pandas for tabular data",
                    "Prefer method chaining for readability",
                    "Add comments for complex operations",
                    "Follow PEP 8 style guide",
                    "Use meaningful variable names"
                ]
            }
        }
        
        self.system_prompt = f"""You are an expert {target_language} developer.

Your job: Generate production-quality, IDIOMATIC {target_language} code from high-level intentions.

CRITICAL RULES:
1. Write IDIOMATIC {target_language} code (not translated syntax from another language)
2. Use appropriate libraries (pandas, numpy, matplotlib for Python)
3. Include necessary imports at the top
4. Add brief comments explaining each major step
5. Follow {target_language} style guides and conventions
6. Make code clean, readable, and maintainable

DO NOT:
- Translate syntax literally from the source language
- Use non-idiomatic patterns
- Add unnecessary complexity

Think: "How would a professional {target_language} developer solve this?"

Output ONLY the code. No explanations before or after the code block."""

    def generate(self, intent_graph, original_code=None, source_language=None):
        """
        Generate target language code from intent graph.
        
        Args:
            intent_graph (dict): Intent graph from Intent Extractor
            original_code (str, optional): Original source code for context
            source_language (str, optional): Source language name
            
        Returns:
            str: Generated code in target language
        """
        
        print(f"\n⚡ [Code Generator] Generating {self.target_language} code...")
        
        # Get language profile
        profile = self.language_profiles.get(self.target_language, {})
        
        # Build the prompt
        user_prompt = f"""Generate {self.target_language} code based on these intentions:

INTENTIONS:
{json.dumps(intent_graph, indent=2)}

LANGUAGE PROFILE:
{json.dumps(profile, indent=2)}

OVERALL GOAL: {intent_graph.get('overall_goal', 'Process and analyze data')}

{f"ORIGINAL {source_language} CODE (for context only - DO NOT translate directly):" if original_code else ""}
{f"```{source_language}" if source_language else ""}
{original_code if original_code else ""}
{f"```" if original_code else ""}

Generate clean, idiomatic {self.target_language} code that accomplishes the same goal.
Write as a native {self.target_language} developer would, not as a translation.

Output ONLY the code:"""

        messages = [
            SystemMessage(content=self.system_prompt),
            HumanMessage(content=user_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Clean up the generated code
        generated_code = response.content.strip()
        
        # Remove markdown code blocks if present
        if generated_code.startswith("```python"):
            generated_code = generated_code.split("```python")[1]
        elif generated_code.startswith("```"):
            lines = generated_code.split("\n")
            generated_code = "\n".join(lines[1:-1]) if len(lines) > 2 else generated_code
        
        if generated_code.endswith("```"):
            generated_code = generated_code.rsplit("```", 1)[0]
        
        generated_code = generated_code.strip()
        
        # Count lines
        line_count = len(generated_code.split("\n"))
        
        print(f"✅ Generated {line_count} lines of {self.target_language} code")
        
        return generated_code


# ============================================================================
# TEST ALL THREE AGENTS TOGETHER!
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("COMPLETE CODE CONVERSION PIPELINE")
    print("="*70)
    
    # Import other agents
    from parser_agent import ParserAgent
    from intent_extractor import IntentExtractorAgent
    
    # Test R code
    r_code = """
library(dplyr)

# Load sales data
sales_data <- read.csv("sales.csv")

# Calculate average sales by country
country_avg <- sales_data %>%
  group_by(country) %>%
  summarise(avg_sales = mean(sales))

print(country_avg)
"""
    
    print("\n📋 ORIGINAL R CODE:")
    print("-" * 70)
    print(r_code)
    print("-" * 70)
    
    # STEP 1: Parse
    print("\n🔄 STEP 1: Parsing code structure...")
    parser = ParserAgent()
    parsed = parser.parse(r_code, "R")
    
    # STEP 2: Extract Intentions
    print("\n🔄 STEP 2: Extracting intentions...")
    extractor = IntentExtractorAgent()
    intentions = extractor.extract_intents(parsed, r_code, "R")
    
    # STEP 3: Generate Python Code
    print("\n🔄 STEP 3: Generating Python code...")
    generator = CodeGeneratorAgent(target_language="Python")
    python_code = generator.generate(intentions, r_code, "R")
    
    # Show final result
    print("\n" + "="*70)
    print("🎯 GENERATED PYTHON CODE:")
    print("="*70)
    print(python_code)
    print("="*70)
    
    print("\n" + "="*70)
    print("🚀 SUCCESS! THREE AGENTS WORKING TOGETHER!")
    print("="*70)
    print("✓ Step 1: Parser analyzed R code structure")
    print("✓ Step 2: Intent Extractor understood developer goals")
    print("✓ Step 3: Code Generator created idiomatic Python code")
    print("="*70)