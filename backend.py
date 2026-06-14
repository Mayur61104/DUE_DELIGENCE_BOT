# query search for links thru serper
import json
import requests
import trafilatura
from dotenv import load_dotenv
import os

try:
    import streamlit as st

    key2 = st.secrets["GROQ_API_KEY"]
    key = st.secrets["SERPER_API_KEY"]

except Exception:
    from dotenv import load_dotenv

    load_dotenv()

    key2 = os.getenv("GROQ_API_KEY")
    key = os.getenv("SERPER_API_KEY")
def query_search(q):
    url = "https://google.serper.dev/search"

    payload = json.dumps({
        "q": q
    })

    headers = {
        'X-API-KEY': key,
        'Content-Type': 'application/json'
    }

    response = requests.post(
        url,
        headers=headers,
        data=payload
    )
    return response.json()


# extracting link from response
def extract_info(data):
    data = data["organic"]
    relevants = []
    for result in data:
        relevants.append({
                "title": result.get("title", ""),
                "snippet": result.get("snippet", ""),
                "link": result.get("link", "")
            })
    return relevants


def valid_link(url):

    try:

        downloaded = trafilatura.fetch_url(url)

        if downloaded is None:
            return False

        text = trafilatura.extract(downloaded)

        if text is None:
            return False

        if len(text) < 300:
            return False

        return True

    except:
        return False


def filter_working_links(results):

    working = []

    BAD_KEYWORDS = [
        "forecast",
        "prediction",
        "price-target",
        "stock-forecast",
        "analyst-predictions"
    ]

    BAD_DOMAINS = [
        "reddit.com",
        "wikipedia.org",
        "quizlet.com"
    ]

    for result in results:

        link = result["link"].lower()
        title = result["title"].lower()

        # Remove bad domains
        if any(domain in link for domain in BAD_DOMAINS):
            continue

        # Remove forecast / prediction content
        if any(keyword in link for keyword in BAD_KEYWORDS):
            continue

        if any(keyword in title for keyword in BAD_KEYWORDS):
            continue

        if valid_link(link):

            working.append(result)

        if len(working) == 3:
            break

    return working


# extracting articles from link
def extract_article(links):

    extracted_articles = []

    for link in links:

        try:

            downloaded = trafilatura.fetch_url(link)

            if downloaded is None:
                continue

            text = trafilatura.extract(downloaded)

            if text and len(text) > 300:
                extracted_articles.append(text[:1500])

        except:
            continue

    return extracted_articles


#financial data
def financial_data(query):
  import yfinance as yf
  dat = yf.Ticker(query)
  financial_data = dat.info
  return financial_data


# relevant financials
def relevant_financials(financial_data):
    importants = [
        "marketCap",
        "industry",
        "sector",
        "totalRevenue",
        "trailingPE",
        "fullTimeEmployees",
        "enterpriseValue",
        "profitMargins",
        "operatingMargins",
        "returnOnEquity",
        "debtToEquity"
    ]

    output = {}

    for key in importants:
        output[key] = financial_data.get(key, "Not Available")

    return output



def build_section_text(section_name, serper_relevant, traf_text):

    section_text = ""

    for i, source in enumerate(serper_relevant[section_name]):

        article = (
            traf_text[section_name][i]
            if i < len(traf_text[section_name])
            else "Article not retrieved"
        )

        section_text += f"""
SOURCE {i+1}

TITLE:
{source['title']}

SNIPPET:
{source['snippet']}

ARTICLE:
{article}

----------------------------------------
"""

    return section_text


def summarize_section(
    section_name,
    serper_relevant,
    traf_text
):
    client = Groq(api_key=key2)
    raw_text = build_section_text(
        section_name,
        serper_relevant,
        traf_text
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """
                You are a research analyst.

                Summarize the provided sources into:
                - Key Facts
                - Important Developments
                - Risks (if present)
                - Opportunities (if present)

                Use concise bullet points.
                Do not invent information.
                """
            },
            {
                "role": "user",
                "content": raw_text[:5000]
            }
        ],
        temperature=0.1,
        max_tokens=500
    )

    return response.choices[0].message.content

def generate(input_query):
    from groq import Groq
    client = Groq(api_key=key2)
    serper_relevant = {}
    serper_results = {}
    serper_links = {}
    serper_res = {}
    traf_text = {}
    ticker_map = {
    "NVIDIA": "NVDA",
    "MICROSOFT": "MSFT",
    "AMAZON": "AMZN",
    "APPLE": "AAPL",
    "TESLA": "TSLA",
    "META": "META",
    "ALPHABET": "GOOGL",
    "INFOSYS": "INFY",
    "TCS": "TCS.NS",
    "RELIANCE": "RELIANCE.NS"
    }
    company_name = input_query.upper()
    company_name = ticker_map.get(company_name, company_name)
    queries = {
    "overview":
        f"{input_query} business model products services company overview",

    "competitors":
        f"{input_query} competitors competitive landscape market rivals",

    "news":
        f"{input_query} latest news recent developments announcements",

    "risks":
        f"{input_query} risks challenges threats regulatory issues competition",

    "opportunities":
        f"{input_query} growth opportunities expansion strategy future outlook",

    "management":
        f"{input_query} CEO leadership executive team management governance",
    }
    #raw response json
    for section, q in queries.items():
      serper_res[section] = query_search(q)

    #relevants -  links, snippets , title and also filter results with working links
    for section, results in serper_res.items():
        serper_relevant[section] = filter_working_links(extract_info(results))
        serper_links[section] = [result["link"] for result in serper_relevant[section]]

    # extract text from links
    for section, links in serper_links.items():
        traf_text[section] = extract_article(links)

    #financial data
    yfinance_res = financial_data(company_name)

    #financial relevants
    financial_relevants = relevant_financials(yfinance_res)

    #building text from source,title , snippet and traf_text and then summary
    overview_summary = summarize_section(
    "overview",
    serper_relevant,
    traf_text
)

    competitor_summary = summarize_section(
        "competitors",
        serper_relevant,
        traf_text
    )

    news_summary = summarize_section(
        "news",
        serper_relevant,
        traf_text
    )

    risk_summary = summarize_section(
        "risks",
        serper_relevant,
        traf_text
    )

    opportunity_summary = summarize_section(
        "opportunities",
        serper_relevant,
        traf_text
    )

    management_summary = summarize_section(
        "management",
        serper_relevant,
        traf_text
    )

    #total sources
    total_sources = sum(
    len(serper_relevant[section])
    for section in serper_relevant
    )

    #total sources
    total_sources = sum(
    len(serper_relevant[section])
    for section in serper_relevant
    )

    #sources title
    source_titles = set()

    for section in serper_relevant:
        for source in serper_relevant[section]:
            source_titles.add(source["title"])

    #percentages financial

    def format_percentage(value):
        if isinstance(value, (int, float)):
            return round(value * 100, 2)
        return "Not Available"
    
    profit_margin = format_percentage(
        financial_relevants.get("profitMargins")
    )
    
    operating_margin = format_percentage(
        financial_relevants.get("operatingMargins")
    )
    
    roe = format_percentage(
        financial_relevants.get("returnOnEquity")
    )


    #metadata

    from datetime import datetime

    report_metadata = f"""
    Company: {input_query}

    Report Generated:
    {datetime.now().strftime("%Y-%m-%d %H:%M")}

    Sources Reviewed:
    {total_sources}
    """


    #context building

    context = f"""

    ====================
    SOURCE TITLES
    ====================
    {source_titles}

    no. of sources : {total_sources}

    report metadata : {report_metadata}

    ====================
    COMPANY OVERVIEW
    ====================

    {overview_summary}

    ====================
    COMPETITIVE LANDSCAPE
    =====================

    {competitor_summary}

    ====================
    RECENT NEWS
    ===========

    {news_summary}

    ====================
    RISKS
    =====

    {risk_summary}

    ====================
    OPPORTUNITIES
    =============

    {opportunity_summary}


    ====================
    MANAGEMENT
    =============

    {management_summary}


    ====================
    FINANCIAL DATA
    ==============

    profit_margin : {profit_margin}%

    operating_margin : {operating_margin}%

    return of equity : {roe}%

    {financial_relevants}
    """

    prompt = f"""
    You are a professional private equity analyst preparing a due diligence memo.

    Your task is to generate a report STRICTLY using information provided in the context.

    ====================
    CORE RULES
    ==========

    1. Use ONLY information explicitly present in the context.
    2. Do NOT use external knowledge.
    3. Do NOT invent facts, metrics, rankings, market share figures, management details, business descriptions, forecasts, or financial information.
    4. If information is unavailable, explicitly state:
       "Information not available in retrieved sources."
    5. Treat article content, snippets, source titles, and financial data as valid source material.
    6. Do NOT provide investment recommendations, ratings, buy/sell opinions, valuation opinions, or price targets.
    7. Do NOT make assumptions or infer facts not directly supported by retrieved sources.
    8. If multiple sources conflict, acknowledge the discrepancy.
    9. Use financial metrics exactly as supplied.
    10. Do NOT calculate, estimate, annualize, extrapolate, or derive new financial metrics.

    ====================
    EVIDENCE RULES
    ==============

    1. Every Risk must contain:

       * Risk
       * Supporting Evidence

    2. Every Opportunity must contain:

       * Opportunity
       * Supporting Evidence

    3. Every statement involving:

       * market share
       * industry leadership
       * competitive ranking
       * market dominance
       * competitor comparisons

       MUST begin with:

       "Retrieved sources indicate..."

       OR

       "One retrieved source states..."

    4. If a claim appears to originate from a single retrieved source, prefer:

       "One retrieved source states..."

    5. Every numerical claim must begin with:

       "Retrieved sources indicate..."

    6. Avoid predictive language such as:

       * will
       * likely to
       * expected to
       * projected to

       unless explicitly stated in retrieved sources.

    ====================
    SECTION-SPECIFIC RULES
    ======================

    Executive Summary:

    * Provide a concise company description.
    * Summarize the 2-3 most important opportunities.
    * Summarize the 2-3 most important risks.
    * Include number of sources reviewed if available.
    * Do NOT repeat detailed findings.

    Management & Leadership:

    * Include leadership roles and executives only.
    * Do NOT include executive compensation unless specifically relevant in retrieved sources.

    Financial Overview:

    * Present financial metrics exactly as supplied.
    * Do not interpret financial performance beyond retrieved evidence.

    Competitive Landscape:

    * Separate retrieved facts from claims made by retrieved sources.
    * Any market-share statement must be qualified using the evidence rules above.

    Recent Developments:

    * Include only recent events explicitly mentioned in retrieved sources.
    * Avoid commentary or predictions.

    Opportunities:
    For each opportunity provide:

    Opportunity: <finding>

    Supporting Evidence: <evidence from retrieved sources>

    Risks:
    For each risk provide:

    Risk: <finding>

    Supporting Evidence: <evidence from retrieved sources>

    Missing Information:
    Categorize missing information where possible:

    * Financial
    * Commercial
    * Operational
    * Strategic

    ====================
    REPORT STRUCTURE
    ================

    ## 1. Executive Summary

    ## 2. Company Overview

    ## 3. Business Model

    ## 4. Financial Overview

    ## 5. Competitive Landscape

    ## 6. Management & Leadership

    ## 7. Recent Developments

    ## 8. Opportunities

    ## 9. Risks

    ## 10. Missing Information

    ## 11. Sources Used

    ====================
    SOURCES USED
    ============

    * List unique source titles only.
    * Remove duplicates.
    * Do not invent source names.
    * Do not include sources not present in the context.

    ====================
    OUTPUT REQUIREMENTS
    ===================

    * Use clear headings.
    * Use bullet points where appropriate.
    * Avoid repetition across sections.
    * Be concise and professional.
    * Ensure every statement can be traced to retrieved information.
    * Write in the style of a professional consulting or due diligence memo.

    CONTEXT:

    {context}


    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert due diligence analyst specializing in private equity and market research."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.1,
        max_tokens=2500
    )

    report = response.choices[0].message.content

    return report










