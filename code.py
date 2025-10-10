SYSTEM: You are a helpful assistant that maps business metrics to their associated internal dashboard URL. Your task is to analyze the provided Key Performance Indicators (KPIs), dashboard title, and description, and return *only* the single, most relevant dashboard URL.

If a definitive match is not found based on the input, return the special string "NO_MATCH_FOUND".

## Knowledge Base (Dashboard Mappings)
Dashboard 1:
  Title: Regional Sales Performance
  Description: Key metrics for sales team activity and revenue across EMEA, APAC, and AMER.
  KPIs: Total Revenue, New Customers, Average Deal Size, Sales Cycle Length
  URL: https://internal.dashboard.com/sales/regional-summary

Dashboard 2:
  Title: Website Traffic and Engagement
  Description: Focuses on user behavior, page views, and conversion rates from organic and paid channels.
  KPIs: Daily Active Users (DAU), Bounce Rate, Conversion Rate, Page Views per Session
  URL: https://internal.dashboard.com/marketing/web-analytics

Dashboard 3:
  Title: Customer Support Overview
  Description: Tracks helpdesk efficiency, resolution times, and customer satisfaction scores.
  KPIs: First Response Time, Customer Satisfaction Score (CSAT), Ticket Volume, Time to Resolution
  URL: https://internal.dashboard.com/support/performance

---

## User Request
Dashboard Title: {dashboard_title}
Dashboard Description: {dashboard_description}
Relevant KPIs: {kpis_list}

## Output Format
[The most relevant URL, or "NO_MATCH_FOUND"]

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate

# Load environment variables (e.g., OPENAI_API_KEY)
load_dotenv()

# --- Step 1: Define the Dashboard Mappings (Knowledge Base) ---
# In a real-world scenario, you would fetch this from a database or a configuration file.
DASHBOARD_KNOWLEDGE_BASE = """
Dashboard 1:
  Title: Regional Sales Performance
  Description: Key metrics for sales team activity and revenue across EMEA, APAC, and AMER.
  KPIs: Total Revenue, New Customers, Average Deal Size, Sales Cycle Length
  URL: https://internal.dashboard.com/sales/regional-summary

Dashboard 2:
  Title: Website Traffic and Engagement
  Description: Focuses on user behavior, page views, and conversion rates from organic and paid channels.
  KPIs: Daily Active Users (DAU), Bounce Rate, Conversion Rate, Page Views per Session
  URL: https://internal.dashboard.com/marketing/web-analytics

Dashboard 3:
  Title: Customer Support Overview
  Description: Tracks helpdesk efficiency, resolution times, and customer satisfaction scores.
  KPIs: First Response Time, Customer Satisfaction Score (CSAT), Ticket Volume, Time to Resolution
  URL: https://internal.dashboard.com/support/performance
"""

# --- Step 2: Construct the Prompt Template ---
PROMPT_TEMPLATE = f"""
SYSTEM: You are a helpful assistant that maps business metrics to their associated internal dashboard URL. Your task is to analyze the provided Key Performance Indicators (KPIs), dashboard title, and description, and return *only* the single, most relevant dashboard URL.

If a definitive match is not found based on the input, return the special string "NO_MATCH_FOUND".

## Knowledge Base (Dashboard Mappings)
{DASHBOARD_KNOWLEDGE_BASE}

---

## User Request
Dashboard Title: {{dashboard_title}}
Dashboard Description: {{dashboard_description}}
Relevant KPIs: {{kpis_list}}

## Output Format
[The most relevant URL, or "NO_MATCH_FOUND"]
"""

# Create the LangChain PromptTemplate object
prompt = PromptTemplate(
    input_variables=["dashboard_title", "dashboard_description", "kpis_list"],
    template=PROMPT_TEMPLATE
)

# --- Step 3: Initialize the LLM and Create the Chain ---
# Use an appropriate model like gpt-3.5-turbo or a more powerful one if needed.
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.0) # Set temp to 0 for reliability/consistency

# Simple chain: Prompt -> LLM
dashboard_link_chain = prompt | llm

# --- Step 4: Run the LLM with Sample Input ---
user_input = {
    "dashboard_title": "Monthly Marketing Report",
    "dashboard_description": "We need to see how many users are coming to the site and if they are converting.",
    "kpis_list": "DAU, Bounce Rate, Conversion Rate"
}

# Invoke the chain
response = dashboard_link_chain.invoke(user_input)

# Extract and clean the result
dashboard_url = response.content.strip()

# --- Step 5: Output the result ---
print(f"User Request:")
print(f"  Title: {user_input['dashboard_title']}")
print(f"  KPIs: {user_input['kpis_list']}")
print("-" * 20)
print(f"LLM Response URL: {dashboard_url}")

# Example of a non-match
user_input_no_match = {
    "dashboard_title": "HR Onboarding Status",
    "dashboard_description": "Track progress of new hires through their first 90 days.",
    "kpis_list": "New Hire Attrition, 90-Day Retention"
}

response_no_match = dashboard_link_chain.invoke(user_input_no_match)
print("\n" + "-" * 20)
print(f"LLM Response for non-match: {response_no_match.content.strip()}")
