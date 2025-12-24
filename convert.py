"""
CODE CONVERTER - Simple Command Line Interface
==============================================

Usage:
    python convert.py input.r output.py

This will convert input.r (R code) to output.py (Python code)
"""

import sys
import os
from parser_agent import ParserAgent
from intent_extractor import IntentExtractorAgent
from code_generator import CodeGeneratorAgent

def convert_code(input_file, output_file, source_lang="R", target_lang="Python"):
    """
    Convert code from one language to another.
    
    Args:
        input_file (str): Path to source code file
        output_file (str): Path to save generated code
        source_lang (str): Source language
        target_lang (str): Target language
    """
    
    print("="*70)
    print(f"CODE CONVERTER: {source_lang} → {target_lang}")
    print("="*70)
    
    # Read source code
    print(f"\n📖 Reading {input_file}...")
    try:
        with open(input_file, 'r') as f:
            source_code = f.read()
        print(f"✅ Read {len(source_code)} characters")
    except FileNotFoundError:
        print(f"❌ ERROR: File '{input_file}' not found!")
        return False
    
    # Initialize agents
    print("\n🤖 Initializing agents...")
    parser = ParserAgent()
    extractor = IntentExtractorAgent()
    generator = CodeGeneratorAgent(target_language=target_lang)
    print("✅ All agents ready!")
    
    # Step 1: Parse
    print("\n🔄 Step 1/3: Parsing code structure...")
    parsed = parser.parse(source_code, source_lang)
    
    # Step 2: Extract Intentions
    print("\n🔄 Step 2/3: Extracting intentions...")
    intentions = extractor.extract_intents(parsed, source_code, source_lang)
    
    # Step 3: Generate Code
    print("\n🔄 Step 3/3: Generating code...")
    generated_code = generator.generate(intentions, source_code, source_lang)
    
    # Save output
    print(f"\n💾 Saving to {output_file}...")
    try:
        with open(output_file, 'w') as f:
            f.write(generated_code)
        print(f"✅ Saved {len(generated_code)} characters")
    except Exception as e:
        print(f"❌ ERROR saving file: {e}")
        return False
    
    # Success!
    print("\n" + "="*70)
    print("🎉 CONVERSION COMPLETE!")
    print("="*70)
    print(f"✓ Source: {input_file} ({source_lang})")
    print(f"✓ Output: {output_file} ({target_lang})")
    print(f"✓ Generated {len(generated_code.split(chr(10)))} lines of code")
    print("="*70)
    
    return True


def main():
    """Main entry point for CLI"""
    
    # Check arguments
    if len(sys.argv) < 3:
        print("Usage: python convert.py <input_file> <output_file>")
        print("\nExample:")
        print("  python convert.py my_script.r my_script.py")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    # Detect languages from file extensions
    source_lang = "R" if input_file.endswith('.r') or input_file.endswith('.R') else "Unknown"
    target_lang = "Python" if output_file.endswith('.py') else "Unknown"
    
    # Convert
    success = convert_code(input_file, output_file, source_lang, target_lang)
    
    if success:
        print("\n✨ Try running your generated code!")
        sys.exit(0)
    else:
        print("\n❌ Conversion failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()