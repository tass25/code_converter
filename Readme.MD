# 🚀 Intentions-Based Code Converter

> AI-powered multi-agent system that understands what your code *does* and recreates it idiomatically in another language.

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange)](https://groq.com/)

---

## 🎯 What Makes This Different?

**Traditional approach** (syntax translation):
```
R: group_by(country) → Python: groupby('country')
```

**Our approach** (semantic understanding):
```
R code → "Group data by categorical column" → Idiomatic Python code
```

The system extracts developer **intentions** in a language-agnostic format, then generates clean, production-ready code in the target language.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 **Intentions-Based** | Understands *what* code does, not just *how* it's written |
| 🤖 **Multi-Agent System** | 4 specialized AI agents working together with feedback loops |
| ✅ **Auto-Validation** | Quality checks with automatic retry logic |
| 🌐 **REST API** | FastAPI backend with interactive Swagger documentation |
| 📊 **Real-Time Monitoring** | Elasticsearch dashboard tracking all conversions |
| 🐳 **Docker Ready** | One-command deployment with docker-compose |
| 🎯 **Production Quality** | Generates idiomatic, well-documented code |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INPUT (R Code)                      │
└─────────────────────────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │     🔍 PARSER AGENT                     │
        │  Analyzes code structure (AST, syntax)  │
        └─────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │     🧠 INTENT EXTRACTOR AGENT           │
        │  Extracts language-agnostic intentions  │
        └─────────────────────────────────────────┘
                              ↓
        ┌─────────────────────────────────────────┐
        │     ✅ VALIDATOR AGENT                  │
        │  Checks completeness & consistency      │
        └─────────────────────────────────────────┘
                              ↓
                    (Retry loop if needed)
                              ↓
        ┌─────────────────────────────────────────┐
        │     ⚡ CODE GENERATOR AGENT             │
        │  Creates idiomatic Python code          │
        └─────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 GENERATED CODE (Python)                      │
└─────────────────────────────────────────────────────────────┘
```

**Orchestrated by LangGraph** with state management and conditional flows.

---

## 📊 Real-Time Dashboard

![Dashboard Screenshot](./assets/dashboard.png)

Monitor your conversions in real-time:
- ✅ Total conversions and success rate
- ⚡ Average processing time
- 📈 Conversion trends by language
- 🔍 Detailed logs in Elasticsearch

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Docker** (optional but recommended)
- **Groq API Key** - Get free at [console.groq.com](https://console.groq.com/)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/tass25/code_converter.git
cd code-converter

# 2. Create virtual environment
python -m venv codec
source codec/bin/activate  # Windows: codec\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# 5. Test the system
python workflow.py
```

### Using Docker (Recommended)

```bash
# Start everything (API + Elasticsearch)
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f api

# Access services:
# - API: http://localhost:8000
# - API Docs: http://localhost:8000/docs
# - Elasticsearch: http://localhost:9200
# - Dashboard: Open dashboard.html in browser
```

---

## 💻 Usage Examples

### Command Line Interface

```bash
# Convert a single file
python convert.py input.r output.py

# Example with your R script
python convert.py test_script.r test_script.py
```

### REST API

**Using curl:**
```bash
curl -X POST "http://localhost:8000/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "library(dplyr)\ndata % filter(age > 18)",
    "source_language": "R",
    "target_language": "Python",
    "max_iterations": 3
  }'
```

**Using Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/convert",
    json={
        "source_code": "x <- c(1,2,3)\nmean(x)",
        "source_language": "R",
        "target_language": "Python"
    }
)

print(response.json()["generated_code"])
```

**Interactive API Docs:**
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for Swagger UI

---

## 📁 Project Structure

```
code-converter/
├── 🤖 Agents
│   ├── parser_agent.py           # Analyzes code structure
│   ├── intent_extractor.py       # Extracts developer intentions
│   ├── validator_agent.py        # Validates intention quality
│   └── code_generator.py         # Generates target code
│
├── 🔄 Orchestration
│   ├── workflow.py                # LangGraph state machine
│   └── convert.py                 # CLI interface
│
├── 🌐 API
│   └── api.py                     # FastAPI REST endpoints
│
├── 📊 Monitoring
│   ├── elasticsearch_logger.py    # Centralized logging
│   ├── dashboard.html            # Real-time dashboard
│   └── view_logs.py              # CLI log viewer
│
├── 🐳 Deployment
│   ├── Dockerfile                 # Container definition
│   ├── docker-compose.yml        # Multi-service setup
│   └── requirements.txt          # Python dependencies
│
├── 📝 Configuration
│   ├── .env                       # Environment variables (not in git)
│   ├── .gitignore                # Git ignore rules
│   └── README.md                 # This file
│
└── 🧪 Testing
    ├── test_script.r              # Sample R code
    ├── test_script.py             # Generated Python
    └── test_setup.py              # System tests
```

---

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required
GROQ_API_KEY=your_groq_api_key_here

# Optional
ELASTICSEARCH_HOST=localhost:9200
MAX_ITERATIONS=3
API_HOST=0.0.0.0
API_PORT=8000
```

### Supported Language Pairs

| From | To | Status |
|------|-----|--------|
| R | Python | ✅ Production |
| Python | R | 🚧 Planned |
| SQL | Python | 🚧 Planned |
| Python | Julia | 🚧 Planned |
| JavaScript | TypeScript | 🚧 Planned |

---

## 📈 Monitoring & Observability

### Elasticsearch Dashboard

1. **Start services:** `docker-compose up -d`
2. **Open dashboard:** `dashboard.html` in your browser
3. **View stats:** http://localhost:8000/stats

### Command-Line Monitoring

```bash
# View detailed logs
python view_logs.py

# Query Elasticsearch directly
curl "http://localhost:9200/conversions/_search?pretty&size=5"

# Get statistics via API
curl "http://localhost:8000/stats?hours=24"
```

### What Gets Logged

- ✅ Every conversion request and result
- ⚡ Processing time and iteration count
- 🤖 Individual agent activities and outputs
- ❌ Errors with full context for debugging
- 📊 Performance metrics and trends

---

## 🧪 Testing

### Test Individual Agents

```bash
# Test each agent separately
python parser_agent.py
python intent_extractor.py
python validator_agent.py
python code_generator.py
```

### Test Complete Workflow

```bash
# Full pipeline with all agents
python workflow.py

# CLI conversion
python convert.py test_script.r output.py
```

### Initialize Logging

```bash
# Create Elasticsearch indices and test logging
python elasticsearch_logger.py
```

---

## 📖 API Documentation

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/languages` | Supported languages |
| GET | `/stats` | Conversion statistics |
| POST | `/convert` | Convert code (JSON) |
| POST | `/convert/file` | Convert uploaded file |

### Example Response

```json
{
  "success": true,
  "generated_code": "import pandas as pd\n\ndata = pd.read_csv('file.csv')",
  "intent_graph": {
    "intents": [
      {
        "id": "intent_1",
        "type": "data_loading",
        "description": "Load data from CSV file"
      }
    ],
    "overall_goal": "Load and process data file"
  },
  "validation_result": {
    "valid": true,
    "issues": []
  },
  "iterations": 1,
  "processing_time": 2.34
}
```

---

## 🎓 How It Works (Technical Details)

### 1. Parser Agent
- Uses LLM to analyze code structure
- Extracts: variables, operations, libraries, control flow
- Outputs structured JSON with syntactic elements

### 2. Intent Extractor (Core Innovation)
- Transforms syntax into semantic intentions
- Language-agnostic representation
- Example: `group_by(x)` → "Group data by categorical column"

### 3. Validator Agent
- Checks intention completeness
- Validates dependencies and data flow
- Triggers retry if issues found

### 4. Code Generator
- Uses language profiles for idiomatic patterns
- Generates production-quality code
- Follows target language best practices

### 5. LangGraph Orchestration
- Manages state across agents
- Implements feedback loops
- Handles retries and error recovery

---

## 🚀 Advanced Usage

### Adding a New Language

1. **Create language profile:**

```python
# In code_generator.py, add to language_profiles:
"Julia": {
    "data_loading": "Use CSV.read() or DataFrames.jl",
    "grouping": "Use groupby() from DataFrames",
    "best_practices": [
        "Use DataFrames.jl for tabular data",
        "Leverage Julia's speed with vectorization"
    ]
}
```

2. **Test conversion:**

```bash
# Modify api.py to add "Julia" to supported languages
python convert.py script.r script.jl
```

### Batch Conversion

```bash
# Convert all R files in a directory
for file in *.r; do
    python convert.py "$file" "${file%.r}.py"
done
```

### Custom Validation Rules

Edit `validator_agent.py` to add custom checks:

```python
# Add in validate() method
if not any(intent['type'] == 'data_loading' for intent in intents):
    issues.append({
        "type": "missing_operation",
        "severity": "warning",
        "description": "No data loading operation found"
    })
```

---

## 🐛 Troubleshooting

### Common Issues

**Problem:** Groq API key not working
```bash
# Solution: Check your .env file
cat .env
# Test connection
python test_setup.py
```

**Problem:** Elasticsearch not connecting
```bash
# Solution: Check if Elasticsearch is running
curl http://localhost:9200/_cluster/health
docker-compose ps
```

**Problem:** Conversion fails repeatedly
```bash
# Solution: Check validation logs
python view_logs.py
# Or reduce max_iterations
python convert.py input.r output.py --max-iterations 1
```

**Problem:** Docker containers not starting
```bash
# Solution: Clean and rebuild
docker-compose down -v
docker-compose up -d --build
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
black .
flake8 .
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **[Groq](https://groq.com/)** - Free, blazing-fast LLM inference
- **[LangChain](https://www.langchain.com/)** - Agent orchestration framework
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - State machine for agents
- **[FastAPI](https://fastapi.tiangolo.com/)** - Modern Python web framework
- **[Elasticsearch](https://www.elastic.co/)** - Logging and analytics

---

## 📧 Contact & Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/tass25/code_converter/issues)

---

## 📊 Project Stats

- **AI Agents**: 4 specialized agents
- **Supported Languages**: 2 (R ↔ Python)
- **API Endpoints**: 6
- **Docker Services**: 2 (API + Elasticsearch)
- **Average Conversion Time**: 3-8 seconds

---

## 🎯 Roadmap

### Phase 1: MVP ✅ (Complete)
- [x] Multi-agent system with 4 agents
- [x] R to Python conversion
- [x] REST API with documentation
- [x] Elasticsearch logging
- [x] Docker deployment
- [x] Real-time dashboard

### Phase 2: Enhanced Quality (In Progress)
- [ ] Tester Agent for functional equivalence
- [ ] Unit test generation
- [ ] Code similarity metrics
- [ ] Performance benchmarking

### Phase 3: More Languages
- [ ] Python to Julia
- [ ] SQL to Python/R
- [ ] JavaScript to TypeScript
- [ ] Language auto-detection

### Phase 4: Advanced Features
- [ ] Multi-file project conversion
- [ ] GitHub integration
- [ ] VS Code extension
- [ ] Web-based UI with Monaco editor

---

<div align="center">

**⭐ Star this repo if you find it useful**

Built with ❤️ using AI Agents

[Report Bug](https://github.com/tass25/code_converter/issues) · 
[Request Feature](https://github.com/tass25/code_converter/issues) · 

</div>
