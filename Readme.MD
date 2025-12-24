# 🚀 Intentions-Based Code Converter

AI-powered multi-agent system for converting code between programming languages using semantic understanding.

## ✨ Features

- **🧠 Intentions-Based Conversion**: Extracts developer intent, not just syntax
- **🤖 Multi-Agent System**: 4 specialized AI agents working together
- **🔄 Feedback Loops**: Automatic quality validation with retry logic
- **🌐 REST API**: FastAPI backend with automatic documentation
- **📊 Monitoring**: Prometheus + Grafana dashboards
- **📝 Logging**: ELK Stack for comprehensive debugging
- **🐳 Docker**: One-command deployment
- **🎯 High Quality**: Generates idiomatic, production-ready code

## 🏗️ Architecture

```
User Input (R Code)
       ↓
┌──────────────────┐
│  Parser Agent    │  → Analyzes code structure
└──────────────────┘
       ↓
┌──────────────────┐
│ Intent Extractor │  → Extracts developer goals
└──────────────────┘
       ↓
┌──────────────────┐
│ Validator Agent  │  → Checks completeness
└──────────────────┘
       ↓ (retry loop if needed)
┌──────────────────┐
│ Generator Agent  │  → Creates Python code
└──────────────────┘
       ↓
Generated Code (Python)
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Docker (optional)
- Groq API key (free at https://console.groq.com/)

### 1. Clone and Setup

```bash
# Clone repository
git clone https://github.com/tass25/code_converter.git
cd code-converter

# Create virtual environment
python -m venv codec
source codec/bin/activate  # On Windows: codec\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your API key
echo "GROQ_API_KEY=your_key_here" > .env
```

### 2. Test Individual Agents

```bash
# Test Parser Agent
python parser_agent.py

# Test Intent Extractor
python intent_extractor.py

# Test Validator
python validator_agent.py

# Test Code Generator
python code_generator.py
```

### 3. Test Complete Workflow

```bash
# Test LangGraph workflow with all agents
python workflow.py
```

### 4. Use Command-Line Interface

```bash
# Convert a file
python convert.py input.r output.py

# Example
python convert.py test_script.r test_script.py
```

### 5. Start API Server

```bash
# Run FastAPI server
python api.py

# API will be available at:
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

### 6. Test API

```bash
# Using curl
curl -X POST "http://localhost:8000/convert" \
  -H "Content-Type: application/json" \
  -d '{
    "source_code": "data <- read.csv(\"file.csv\")\nmean(data$value)",
    "source_language": "R",
    "target_language": "Python"
  }'

# Or visit http://localhost:8000/docs for interactive API docs
```

## 🐳 Docker Deployment

### Full Stack (API + Monitoring)

```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop all services
docker-compose down
```

### Services

After running `docker-compose up -d`:

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Prometheus**: http://localhost:9090
- **Grafana**: http://localhost:3000 (admin/admin)
- **Kibana**: http://localhost:5601

## 📁 Project Structure

```
code-converter/
├── parser_agent.py           # Agent 1: Code structure analysis
├── intent_extractor.py       # Agent 2: Intention extraction
├── validator_agent.py        # Agent 3: Quality validation
├── code_generator.py         # Agent 4: Code generation
├── workflow.py               # LangGraph workflow orchestration
├── api.py                    # FastAPI REST API
├── convert.py                # CLI interface
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker container
├── docker-compose.yml        # Multi-container setup
├── .env                      # Environment variables (API keys)
├── .gitignore               # Git ignore rules
├── monitoring/
│   ├── prometheus.yml       # Prometheus config
│   └── grafana-dashboards/  # Grafana dashboards
└── tests/                   # Test files
```

## 🔧 Configuration

### Supported Languages

**Current (MVP)**:
- R → Python ✅
- Python → R ✅

**Planned**:
- Python → Julia
- SQL → Python
- JavaScript → TypeScript

### Environment Variables

```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here

# Optional
MAX_ITERATIONS=3
API_HOST=0.0.0.0
API_PORT=8000
```

### Customization

#### Add New Language

1. Create language profile in `languages/` folder:

```yaml
# languages/julia.yaml
language: Julia
parser: tree-sitter-julia
data_structures:
  - DataFrame
  - Array
operations:
  - groupby: combine() with grouping
  - aggregate: aggregate() function
best_practices:
  - "Use DataFrames.jl for tabular data"
  - "Leverage Julia's speed for numerical operations"
```

2. Update `code_generator.py` language profiles

3. Test conversion!

## 📊 Monitoring

### Grafana Dashboards

Access Grafana at http://localhost:3000:

- **Overview**: Conversion volumes, success rates
- **Agent Performance**: Latency and success by agent
- **System Health**: Resource usage, error rates

### Prometheus Metrics

Access Prometheus at http://localhost:9090:

- `conversions_total` - Total conversions by language pair
- `agent_duration_seconds` - Agent processing time
- `validation_failures_total` - Validation failure count

### Kibana Logs

Access Kibana at http://localhost:5601:

- Full agent conversations
- Error traces with context
- Intent graphs for debugging

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_parser.py

# Run with coverage
pytest --cov=. tests/
```

## 📖 API Documentation

### POST /convert

Convert code from source to target language.

**Request:**
```json
{
  "source_code": "library(dplyr)\ndata <- read.csv('file.csv')",
  "source_language": "R",
  "target_language": "Python",
  "max_iterations": 3
}
```

**Response:**
```json
{
  "success": true,
  "generated_code": "import pandas as pd\ndata = pd.read_csv('file.csv')",
  "intent_graph": {...},
  "validation_result": {...},
  "iterations": 1,
  "processing_time": 3.45
}
```

### POST /convert/file

Upload and convert a code file.

**Request:**
- Form data with file upload
- Query params: `target_language`, `max_iterations`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- **Groq** for free, blazing-fast LLM API
- **LangChain/LangGraph** for agent orchestration
- **Anthropic** for Claude and prompt engineering guidance

## 📧 Contact

For questions or issues, please open a GitHub issue.

---

**Built with ❤️**