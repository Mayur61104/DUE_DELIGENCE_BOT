# 📊 Due Diligence Copilot

An AI-powered research assistant that automates company due diligence by combining web intelligence, financial data enrichment, and Large Language Models (LLMs) to generate structured, investor-style reports in minutes.

---

## Overview

Due Diligence Copilot streamlines the process of researching public and private companies by automatically gathering information from multiple sources, extracting relevant insights, enriching them with financial data, and generating a comprehensive due diligence report.

The platform is designed for:

* Investment Analysts
* Private Equity & Venture Capital Teams
* Management Consultants
* Corporate Strategy Teams
* Market Research Professionals
* Business Analysts

---

## Key Capabilities

### Company Intelligence

Generate structured reports covering:

* Executive Summary
* Company Overview
* Business Model
* Financial Overview
* Competitive Landscape
* Management & Leadership
* Recent Developments
* Opportunities
* Risks
* Missing Information
* Sources Referenced

### Automated Research Pipeline

* Multi-query web retrieval
* Source validation and filtering
* Article extraction and processing
* Financial data enrichment
* AI-driven summarization
* Report generation

### Financial Analysis

Retrieve and summarize key company metrics including:

* Market Capitalization
* Revenue
* Profit Margin
* Operating Margin
* Return on Equity (ROE)
* Debt-to-Equity Ratio
* Sector and Industry Information

### Source-Based Reporting

The system is designed to:

* Use retrieved information only
* Preserve source traceability
* Highlight risks and opportunities with supporting evidence
* Reduce hallucinations through structured retrieval workflows

---

## System Architecture

```text
User Query
    │
    ▼
Serper Search API
    │
    ▼
Link Validation & Filtering
    │
    ▼
Article Extraction (Trafilatura)
    │
    ▼
Section-Level Summarization
    │
    ▼
Yahoo Finance Enrichment
    │
    ▼
Context Construction
    │
    ▼
Groq LLM
    │
    ▼
Due Diligence Report
```

---

## Technology Stack

| Component          | Technology               |
| ------------------ | ------------------------ |
| Frontend           | Streamlit                |
| LLM                | Groq (Llama 3.3 70B)     |
| Search Engine      | Serper API               |
| Financial Data     | Yahoo Finance (yfinance) |
| Content Extraction | Trafilatura              |
| Language           | Python                   |

---

## Features

### Research Retrieval

* Multi-query search strategy
* Company overview retrieval
* Competitor analysis
* Recent news aggregation
* Risk discovery
* Opportunity identification
* Management research

### AI Analysis

* Context-aware summarization
* Source consolidation
* Structured report generation
* Evidence-backed insights

### Reporting

* Professional due diligence format
* Downloadable reports
* Streamlit-based user interface

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd due-diligence-copilot
```

### Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## Run Locally

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

## Example Workflow

1. Enter a company name (e.g., NVIDIA)
2. Retrieve company information from multiple web sources
3. Extract and summarize relevant content
4. Enrich findings with financial data
5. Generate a structured due diligence report
6. Review or download the report

---

## Future Roadmap

### Version 2

* Company-to-company relationship intelligence
* Executive and stakeholder connection mapping
* Risk heatmaps
* Entity relationship graphs
* Due diligence monitoring
* Event-driven alerts
* Multi-company benchmarking
* PDF report export

### Long-Term Vision

Transform the platform from a report generator into an AI-powered Due Diligence Copilot capable of uncovering hidden relationships, governance risks, competitive threats, and strategic opportunities across companies, executives, investors, and corporate networks.

---

## Disclaimer

This project is intended for educational, research, and demonstration purposes.

Generated reports are dependent on retrieved source quality and should not be considered investment, legal, financial, or business advice.

---

## Author

**Mayur Jambhulkar**

IIT Bombay | Metallurgical Engineering and Material Science

Interested in:

* AI & Machine Learning
* Market Intelligence
* Business Analytics
