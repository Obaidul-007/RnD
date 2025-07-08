# Python Flask web application + Playwright + MCP Testing Project

This project demonstrates integration of Playwright testing with MCP (Model Context Protocol) for AI-powered testing of a Python Flask application.

## Features

- Flask web application with task management
- Playwright end-to-end testing
- MCP server for AI-powered test generation
- Automated test case generation based on page analysis
- Responsive design testing
- Accessibility testing

## Quick Start

1. Clone the repository
2. Set up virtual environment: `python -m venv venv && source venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Install Playwright browsers: `playwright install`
5. Start the application: `python src/app.py`
6. Run tests: `pytest tests/`

## MCP Integration

The MCP server provides AI-powered testing tools that can analyze web pages and generate test cases automatically.

## Running Tests

- Basic tests: `pytest tests/test_basic.py`
- AI-powered tests: `pytest tests/test_ai_powered.py`
- All tests: `pytest`
- With HTML report: `pytest --html=reports/report.html`
