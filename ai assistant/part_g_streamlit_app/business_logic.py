from datetime import datetime
from pathlib import Path
import csv
import ast
import operator

from company_data import COMPANY_CONFIG

LEADS_FILE = Path("data") / "leads.csv"
LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)


def get_company_information_logic(topic: str = "general") -> str:
    topic = topic.lower().strip()
    company = COMPANY_CONFIG

    if topic in ["general", "about", "company"]:
        return (
            f"Company Name: {company['company_name']}\n"
            f"About: {company['about']}\n"
            f"Location: {company['location']}\n"
            f"Working Hours: {company['working_hours']}\n"
            f"Email: {company['contact_email']}\n"
            f"Phone: {company['phone']}"
        )

    if topic in ["services", "service"]:
        lines = ["Official services:"]
        for key, service in company["services"].items():
            lines.append(
                f"- {service['display_name']}: {service['description']} "
                f"Starting from ${service['starting_price_usd']}"
            )
        return "\n".join(lines)

    if topic in ["location", "address"]:
        return f"Our office is located in {company['location']}."

    if topic in ["hours", "working hours", "timing", "time"]:
        return f"Our working hours are {company['working_hours']}."

    if topic in ["contact", "email", "phone"]:
        return f"Email: {company['contact_email']} | Phone: {company['phone']}"

    if topic in company["faqs"]:
        return company["faqs"][topic]

    return (
        "I could not find that exact topic in official company data. "
        "Available topics: general, services, location, working hours, contact, payment, timeline, support."
    )


def normalize_service_name(service: str) -> str:
    service = service.lower().strip()
    aliases = {
        "web": "website",
        "site": "website",
        "business website": "website",
        "ai bot": "chatbot",
        "bot": "chatbot",
        "ai chatbot": "chatbot",
        "app": "mobile app",
        "application": "mobile app",
        "vision": "computer vision",
        "cv": "computer vision",
        "automation system": "automation",
    }
    return aliases.get(service, service)


def get_service_price_logic(service: str) -> str:
    service_key = normalize_service_name(service)
    services = COMPANY_CONFIG["services"]

    if service_key not in services:
        available = ", ".join(services.keys())
        return f"Service not found. Available services are: {available}."

    selected = services[service_key]
    return (
        f"{selected['display_name']} starts from "
        f"${selected['starting_price_usd']} USD. "
        f"Description: {selected['description']}"
    )

_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        return _ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPERATORS:
            raise ValueError("Operator not allowed")
        return _ALLOWED_OPERATORS[op_type](operand)
    raise ValueError("Only basic arithmetic is allowed")


def calculator_logic(expression: str) -> str:
    try:
        tree = ast.parse(expression, mode="eval")
        result = _safe_eval(tree.body)
        return str(round(result, 2))
    except Exception as e:
        return f"Calculation error: {e}"


def save_lead_logic(name: str, email: str, requirement: str) -> str:
    name = name.strip()
    email = email.strip()
    requirement = requirement.strip()

    if not name or not email or not requirement:
        return "Lead was not saved. Name, email and requirement are required."

    file_exists = LEADS_FILE.exists()

    with LEADS_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=["timestamp", "name", "email", "requirement"]
        )
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "name": name,
            "email": email,
            "requirement": requirement,
        })

    return f"Lead saved successfully for {name} with email {email}."
