#!/bin/bash

# Code Converter - Complete Setup Script
# This script sets up everything automatically

echo "======================================================================"
echo "🚀 CODE CONVERTER - COMPLETE SETUP"
echo "======================================================================"

# Check Python version
echo ""
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
echo "✓ Python $python_version detected"

# Check if .env exists
if [ ! -f .env ]; then
    echo ""
    echo "⚠️  .env file not found!"
    echo "Please create .env file with:"
    echo "GROQ_API_KEY=your_key_here"
    echo ""
    read -p "Enter your Groq API key: " api_key
    echo "GROQ_API_KEY=$api_key" > .env
    echo "✓ Created .env file"
fi

# Create monitoring directory
echo ""
echo "Creating monitoring directory..."
mkdir -p monitoring
echo "✓ Monitoring directory created"

# Test all agents
echo ""
echo "======================================================================"
echo "TESTING ALL AGENTS"
echo "======================================================================"

echo ""
echo "1️⃣  Testing Parser Agent..."
python3 parser_agent.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Parser Agent: WORKING"
else
    echo "❌ Parser Agent: FAILED"
fi

echo ""
echo "2️⃣  Testing Intent Extractor..."
python3 intent_extractor.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Intent Extractor: WORKING"
else
    echo "❌ Intent Extractor: FAILED"
fi

echo ""
echo "3️⃣  Testing Validator..."
python3 validator_agent.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Validator Agent: WORKING"
else
    echo "❌ Validator Agent: FAILED"
fi

echo ""
echo "4️⃣  Testing Code Generator..."
python3 code_generator.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Code Generator: WORKING"
else
    echo "❌ Code Generator: FAILED"
fi

echo ""
echo "5️⃣  Testing Complete Workflow..."
python3 workflow.py > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ LangGraph Workflow: WORKING"
else
    echo "❌ LangGraph Workflow: FAILED"
fi

echo ""
echo "======================================================================"
echo "✅ SETUP COMPLETE!"
echo "======================================================================"
echo ""
echo "🎯 Quick Start Commands:"
echo ""
echo "  # Convert a file"
echo "  python convert.py test_script.r test_script.py"
echo ""
echo "  # Start API server"
echo "  python api.py"
echo ""
echo "  # Start full stack with Docker"
echo "  docker-compose up -d"
echo ""
echo "  # View API documentation"
echo "  Open http://localhost:8000/docs"
echo ""
echo "======================================================================"
echo "🎉 Happy Converting!"
echo "======================================================================"