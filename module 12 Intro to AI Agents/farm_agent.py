"""
farm_agent.py  -  Module 12: the farm agent built FROM SCRATCH (no framework)
==============================================================================
Designed by Engr Usman Hasan  (Bano Qabil Generative AI course)

This is the same agent as the Day 1 notebook, in one file.
The Streamlit app (streamlit_app.py) imports it.

THE FLOW
  question -> [THINK: ask the LLM] -> Action? -> [ACT: run the Python tool] -> [OBSERVE: send the result back]
           -> repeat ... -> Final Answer          (max_steps = the safety limit)

HOW TO RUN
  pip install -r requirements.txt
  copy .env.example to .env and paste a FREE key (GROQ_API_KEY or GEMINI_API_KEY)
  python farm_agent.py "Ali ko 15 litre doodh chahiye, bill kitna hoga?"
"""

# 'os' reads the API keys from the environment
import os
# 'sys' reads the question you type after the file name
import sys

# python-dotenv copies the keys from the .env file into the environment
from dotenv import load_dotenv

# read the .env file
load_dotenv()
# use Groq if a Groq key exists, otherwise Gemini (you can force one with PROVIDER=gemini in .env)
PROVIDER = os.getenv("PROVIDER") or ("groq" if os.getenv("GROQ_API_KEY") else "gemini")


# ===== THE LLM HELPER: one small function that talks to Groq OR Gemini =====
# the model we use for each provider (change it here if a name is retired)
MODELS = {"groq": "llama-3.3-70b-versatile", "gemini": "gemini-flash-latest"}

# if we chose Groq...
if PROVIDER == "groq":
    # ...import Groq's Python package
    from groq import Groq
    # create a Groq client with our key
    client = Groq(api_key=os.environ["GROQ_API_KEY"])
# otherwise we use Gemini
else:
    # import Google's Python package
    from google import genai
    # create a Gemini client with our key
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


# send a list of messages to the LLM and get its reply text back
def ask_llm(messages, stop=None):
    # ----- Groq -----
    if PROVIDER == "groq":
        # send the whole conversation; temperature=0 means "no random answers"
        reply = client.chat.completions.create(
            # which model
            model=MODELS["groq"],
            # the conversation so far
            messages=messages,
            # no randomness
            temperature=0,
            # stop writing when the model reaches one of these words
            stop=stop,
        )
        # take out the text of the reply
        return reply.choices[0].message.content or ""
    # ----- Gemini -----
    # Gemini wants the system message separately...
    system_text = messages[0]["content"]
    # ...and calls the assistant "model" instead of "assistant"
    contents = [{"role": "model" if m["role"] == "assistant" else "user",
                 # each message's text goes inside "parts"
                 "parts": [{"text": m["content"]}]}
                # every message except the first (system) one
                for m in messages[1:]]
    # send it, with the same settings as Groq
    reply = client.models.generate_content(
        # which model
        model=MODELS["gemini"],
        # the conversation
        contents=contents,
        # system message + no randomness + stop words
        config={"system_instruction": system_text, "temperature": 0, "stop_sequences": stop},
    )
    # the reply text ("" if Gemini sent nothing)
    return reply.text or ""


# ===== THE FARM'S DATA: a tiny pretend database =====
# price of each product in rupees
PRICES = {"milk": 220, "yogurt": 250, "desi ghee": 2600}
# the unit of each product, so answers say "litre" or "kg"
UNITS = {"milk": "litre", "yogurt": "kg", "desi ghee": "kg"}
# how much of each product is in the farm's stock today
STOCK = {"milk": 40, "yogurt": 12, "desi ghee": 3}

# the farm's rules (like the documents we searched in Modules 08 and 09)
FARM_RULES = [
    # rule 1
    "Delivery time: every morning from 6 am to 9 am.",
    # rule 2
    "Delivery areas: DHA, Clifton, Gulshan and PECHS only.",
    # rule 3
    "Delivery charge: Rs 150 per order. Delivery is free when the bill is Rs 3000 or more.",
    # rule 4
    "Bulk discount: 5% off milk when a customer orders 20 litres or more.",
    # rule 5
    "Orders for tomorrow must be placed before 8 pm today.",
    # rule 6
    "Payment: cash on delivery or JazzCash.",
]


# ===== THE TOOLS: normal Python functions the agent is allowed to use =====
# Every tool takes ONE text input and returns ONE text answer.
# The first line inside each function (the """docstring""") is the tool's DESCRIPTION.
# The LLM reads ONLY that description to decide which tool to use. Write it clearly!


# tool 1: the price of a product
def get_price(product):
    """Price of ONE farm product. Input: the product name, e.g. milk, yogurt or desi ghee."""
    # make the input small letters and remove extra spaces ("  Milk " -> "milk")
    name = product.lower().strip()
    # if we don't sell it, say so (and list what we DO sell)
    if name not in PRICES:
        # an answer the agent can read and use
        return f"We don't sell '{product}'. We sell: {', '.join(PRICES)}."
    # otherwise give the price with its unit
    return f"{name}: Rs {PRICES[name]} per {UNITS[name]}"


# tool 2: how much is in stock
def check_stock(product):
    """How much of ONE product is in stock today. Input: the product name, e.g. milk."""
    # clean the input the same way
    name = product.lower().strip()
    # unknown product?
    if name not in STOCK:
        # tell the agent clearly
        return f"We don't sell '{product}'. We sell: {', '.join(STOCK)}."
    # the stock amount with its unit
    return f"{name}: {STOCK[name]} {UNITS[name]} in stock"


# tool 3: a calculator (LLMs are bad at maths, Python is perfect at it)
def calculator(expression):
    """Do maths. Input: a maths expression using numbers and + - * / ( ), e.g. 10 * 220."""
    # only these characters are allowed, so nobody can run dangerous code
    allowed = "0123456789+-*/(). "
    # check every character of the input
    if any(ch not in allowed for ch in expression):
        # refuse anything that is not plain maths
        return "Error: only numbers and + - * / ( ) are allowed."
    # try to calculate it
    try:
        # eval() works out the maths; round to 2 decimal places
        return str(round(eval(expression), 2))
    # e.g. dividing by zero or a broken expression
    except Exception as error:
        # report the problem so the agent can try again
        return f"Error: {error}"


# tool 4: search the farm's rules (a mini version of RAG from Modules 08-09)
def search_farm_rules(question):
    """Search the farm's rules (delivery time, delivery areas, delivery charge, discounts, payment). Input: a short question."""
    # split the question into lowercase words longer than 3 letters ("delivery", "charge", ...)
    words = [w.strip("?.,!") for w in question.lower().split() if len(w) > 3]
    # give every rule a score: how many of the question's words appear in it
    scored = [(sum(w in rule.lower() for w in words), rule) for rule in FARM_RULES]
    # keep the 2 best rules that matched at least one word
    best = [rule for score, rule in sorted(scored, reverse=True)[:2] if score > 0]
    # join them with a new line, or say that nothing matched
    return "\n".join(best) if best else "No rule found for that question."


# the agent's TOOLBOX: tool name -> the Python function to run
TOOLS = {
    # name the LLM will write -> real function
    "get_price": get_price,
    # stock checker
    "check_stock": check_stock,
    # calculator
    "calculator": calculator,
    # rule search
    "search_farm_rules": search_farm_rules,
}


# ===== YOUR TURN: give the agent a NEW tool =====
# delivery charge for each area (from the farm's rules)
DELIVERY_AREAS = {"dha": 150, "clifton": 150, "gulshan": 150, "pechs": 150}


# tool 5: does the farm deliver to an area, and what does it cost?
def delivery_charge(area):
    """Check if the farm delivers to an area and the delivery charge. Input: the area name, e.g. DHA or Clifton."""
    # clean the input: small letters, first word only ("DHA Phase 6" -> "dha")
    name = area.lower().strip().split()[0]
    # we deliver there
    if name in DELIVERY_AREAS:
        # give the charge and the free-delivery rule
        return f"Yes, we deliver to {area}. Charge: Rs {DELIVERY_AREAS[name]} (free if the bill is Rs 3000 or more)."
    # we don't deliver there
    return f"Sorry, we don't deliver to {area}. We deliver to: DHA, Clifton, Gulshan, PECHS."


# put the new tool in the toolbox (the menu updates by itself!)
TOOLS["delivery_charge"] = delivery_charge


# ===== THE TOOL MENU: what the LLM reads to choose a tool =====
# turn the TOOLS dictionary into a menu: one line per tool, "- name: description"
def tool_menu():
    # for every tool, take its name and the docstring we wrote
    return "\n".join(f"- {name}: {func.__doc__}" for name, func in TOOLS.items())


# ===== THE ReAct INSTRUCTIONS (the "system prompt") =====
# ReAct = REason + ACT. We tell the LLM to think out loud, then act, then wait.
# {tools} is a blank that gets filled with the tool menu
REACT_TEMPLATE = """You are the helpful agent of Marhaba Cattle & Dairy Farm in Karachi.

You can use these tools:
{tools}

Always reply in EXACTLY this format:
Thought: what you should do next
Action: the name of ONE tool from the list
Action Input: the input for that tool

Then STOP. The system will run the tool and send you an Observation.
You can repeat Thought / Action / Action Input as many times as you need.

When you know the answer, reply:
Thought: I now know the final answer
Final Answer: the answer for the customer

Rules:
- Never guess prices, stock, rules or maths. Use a tool.
- Use only ONE tool at a time.
- If no tool is needed (e.g. a greeting), go straight to Final Answer.
- Reply in the customer's language (English or Roman Urdu)."""


# fill the blank with the CURRENT tool menu (so new tools appear automatically)
def build_system_prompt():
    # .format() puts the menu where {tools} is written
    return REACT_TEMPLATE.format(tools=tool_menu())


# ===== THE PARSER: read the LLM's reply and find what it wants to do =====
# 're' finds patterns in text
import re


# look at one reply and return (kind, value1, value2)
def parse_reply(reply):
    # case 1: the LLM has the final answer
    if "Final Answer:" in reply:
        # everything after "Final Answer:" is the answer
        return "final", reply.split("Final Answer:")[-1].strip(), None
    # case 2: find the line that starts with "Action:"
    action = re.search(r"Action:\s*(.+)", reply)
    # and the line that starts with "Action Input:"
    action_input = re.search(r"Action Input:\s*(.+)", reply)
    # if both were found, the LLM wants to use a tool
    if action and action_input:
        # return the tool name and its input (without extra quotes or spaces)
        return "tool", action.group(1).strip(), action_input.group(1).strip().strip('"')
    # case 3: the reply is in the wrong format
    return "error", None, None


# ===== THE AGENT LOOP: Think -> Act -> Observe -> repeat =====
# This is the WHOLE secret of an agent: a loop around an LLM.
def run_agent(question, max_steps=6, show=True):
    # the conversation starts with the instructions and the customer's question
    messages = [{"role": "system", "content": build_system_prompt()},
                # the customer's question
                {"role": "user", "content": question}]
    # we save every step here (for printing and for the Streamlit app)
    steps = []
    # print the question
    if show:
        # 🙋 = the customer
        print("🙋 QUESTION:", question)
    # loop at most max_steps times (a safety limit, so it can never loop forever)
    for step in range(1, max_steps + 1):
        # THINK: ask the LLM; stop it before it invents its own "Observation"
        reply = ask_llm(messages, stop=["Observation:"]).strip()
        # read what it wants to do
        kind, value, tool_input = parse_reply(reply)
        # show the LLM's thinking
        if show:
            # the raw Thought / Action lines
            print(f"\n----- step {step} -----\n🧠 {reply}")
        # FINISHED? the LLM gave a final answer
        if kind == "final":
            # remember this step
            steps.append({"step": step, "llm": reply, "observation": None})
            # print the answer
            if show:
                # ✅ = done
                print("\n✅ FINAL ANSWER:", value)
            # stop the loop and return the answer + all steps
            return value, steps
        # ACT: the LLM chose a tool that exists
        if kind == "tool" and value in TOOLS:
            # run the real Python function with the LLM's input
            observation = TOOLS[value](tool_input)
        # the LLM invented a tool name that does not exist
        elif kind == "tool":
            # tell it which tools are real
            observation = f"There is no tool called '{value}'. Use one of: {', '.join(TOOLS)}"
        # the reply was in the wrong format
        else:
            # remind it of the format
            observation = "Wrong format. Reply with Thought / Action / Action Input, or Final Answer."
        # OBSERVE: show what the tool returned
        if show:
            # 👀 = the result the agent sees
            print("👀 Observation:", observation)
        # remember this step
        steps.append({"step": step, "llm": reply, "observation": observation})
        # add the LLM's reply to the conversation...
        messages.append({"role": "assistant", "content": reply})
        # ...and the tool's result, so the LLM can read it in the next loop
        messages.append({"role": "user", "content": f"Observation: {observation}"})
    # we used up all the steps without a final answer
    if show:
        # ⛔ = stopped by the safety limit
        print("\n⛔ Stopped: max_steps reached.")
    # return a polite message + the steps
    return "Sorry, I could not finish. Please ask in a simpler way.", steps


# ===== RUN FROM THE TERMINAL =====
# this part runs only with "python farm_agent.py ...", not when another file imports us
if __name__ == "__main__":
    # the question typed after the file name, or a default question
    question = " ".join(sys.argv[1:]) or "Ali ko kal 15 litre doodh chahiye. Total bill kitna banega, aur kya itna stock hai?"
    # run the agent and print every step
    run_agent(question)

# ===== WHAT TO NOTICE =====
# - The LLM only WRITES which tool it wants. Our loop RUNS the tool.
# - The agent decides how many steps it needs. max_steps stops it if it gets lost.
# ===== YOUR TURN =====
# - Add a new tool function with a clear docstring, then add it to TOOLS. Ask a question that needs it.
