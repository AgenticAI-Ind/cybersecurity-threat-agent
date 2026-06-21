# Cybersecurity Threat Detection Agent

Real-time threat detection with anomaly detection and SIEM integration

## Features

- Production-ready REST API built with FastAPI
- Comprehensive documentation and examples
- Docker support for easy deployment
- Enterprise-grade error handling and logging
- Extensible architecture

## Tech Stack

- **FastAPI**
- **Scikit-learn**
- **ELK Stack**
- **Prometheus**

## Quick Start

### Prerequisites

- Python 3.9+
- Docker & Docker Compose (optional)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/AgenticAI-Ind/cybersecurity-threat-agent.git
cd cybersecurity-threat-agent
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python src/main.py
```

6. Access the API:
- API: http://localhost:8000
- Interactive docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Docker Deployment

```bash
docker-compose up -d
```

## API Documentation

Full API documentation is available at `/docs` when running the application.

## Project Structure

```
cybersecurity-threat-agent/
├── src/
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── models/              # Data models
│   └── services/            # Business logic
├── tests/                   # Test suite
├── docker-compose.yml       # Docker configuration
├── Dockerfile               # Container definition
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Configuration

See `.env.example` for all available configuration options.

## Testing

```bash
pytest tests/ -v --cov=src
```

## License

MIT License - see LICENSE file

## Support

- Documentation: https://useagenticai.in/agents/cybersecurity-threat-agent.html
- Issues: https://github.com/AgenticAI-Ind/cybersecurity-threat-agent/issues
- Email: info@useagenticai.in

## Contributing

Contributions welcome! Please read CONTRIBUTING.md first.
