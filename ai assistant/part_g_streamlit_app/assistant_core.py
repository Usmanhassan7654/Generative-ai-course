import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_agent

from company_data import COMPANY_CONFIG
from tools import tools

load_dotenv()


def build_system_prompt() -> str:
    return f"""
You are the official website assistant for {COMPANY_CONFIG['company_name']}.

Your job:
1. Help website visitors understand the company's services.
2. Never invent company information, prices, policies or timelines.
3. Use get_company_information for company-specific information.
4. Use get_service_price when the user asks about prices, cost, quotation or budget.
5. Use calculator for discounts, percentages and totals.
6. If a visitor shows serious interest, ask for name, email and requirement.
7. Use save_lead only when name, email and requirement are available.
8. Never say a lead was saved unless the save_lead tool succeeded.
9. Keep answers helpful, short and professional.
10. If information is not available, say that you do not have that information.
"""


def create_assistant():
    if not os.getenv("GROQ_API_KEY"):
        raise ValueError("GROQ_API_KEY not found. Add it to .env or Streamlit secrets.")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.2
    )

    return create_agent(
        model=llm,
        tools=tools,
        system_prompt=build_system_prompt()
    )
