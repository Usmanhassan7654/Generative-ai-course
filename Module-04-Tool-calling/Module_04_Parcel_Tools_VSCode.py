# Module 04 — Function Calling and Tool Use
# Prepared by Engr Usman Hasan
# In VS Code use Run Cell above each # %% section.
# First install in the terminal:
# python -m pip install langchain-core==1.6.6 langchain-groq==1.1.3 "python-dotenv>=1,<2" ipykernel
# Run cells top to bottom. Local tool steps need no API key.

# %% [markdown]
# # Module 04: Function Calling and Tool Use
# **Bano Qabil • Prepared by Engr Usman Hasan**
# 
# ## Our learning journey
# **Part A: Maths tools → Part B: Parcel tracking → Class assignment: Book availability**
# 
# First, build addition, subtraction, multiplication and division tools. Let the LLM choose a maths function from the user's question. Then apply the same tool-calling pattern to the parcel tracking project.
# 
# A customer asks: **“Where is my parcel PK101?”** The LLM identifies the tracking number. Our Python function reads a saved status. The LLM explains that returned status.
# 
# This notebook continues Module 3's **ChatGroq**, **ChatPromptTemplate**, and **invoke()**.
# Same Groq-hosted model: `openai/gpt-oss-20b`.
# 
# ## How to use this lab
# 1. Read a step and predict its output.
# 2. Run its short code cell.
# 3. Compare with **Observe** underneath.
# 4. Change the suggested input before continuing.
# 
# You do not write a class, use inheritance, or define Pydantic models. Library objects are ready-made tools that we use through their commands.
# 
# **All parcel records are fictional classroom data. This app has no connection to a courier company.**
# The local function tests need no API key. Live model sections need internet, a private Groq key, model access and available quota.

# %% [markdown]
# ## Open this notebook
# Use Python 3.10 or newer. Install VS Code's Python and Jupyter extensions.
# Open the notebook folder. In the terminal run:
# 
# ```powershell
# python -m venv .venv
# .venv\Scripts\python -m pip install ipykernel
# ```
# 
# Choose **Select Kernel → Python Environments → .venv**.
# Run cells in order, starting with Part A. M1 is ordinary Python; M2–M7 create and test tools locally. M8 onward uses the Groq model. The original parcel steps follow in Part B.

# %% [markdown]
# ## Part A — Start with a maths assistant
# Before parcel tracking, we will make **four tiny tools**: addition, subtraction, multiplication and division.
# 
# You type **“Subtract 4 from 15.”** The LLM chooses `subtract_numbers`, supplies `a=15` and `b=4`, and our Python code calculates the result. The LLM then explains the result.
# 
# **Why use a tool for maths?** The model understands the wording; Python performs the actual calculation. We can inspect which operation ran instead of trusting an unverified generated number.
# 
# *Roman Urdu: Pehle chaar chhotay maths tools banayein ge. User sawal likhe ga, model sahi tool aur numbers choose kare ga, aur Python hisaab kare ga.*
# 
# These new **M1–M16** steps come before the existing parcel labs **1–20**. PPT slides 8–29 cover the maths warm-up. The parcel steps follow on slides 30–58. Each lab heading gives its matching slide number.

# %% [markdown]
# ### M1. Start with an ordinary addition function
# 
# **PPT checkpoint: slides 8**
# Predict the answer to `add(5, 3)` before running.
# 
# | Python piece | Meaning |
# |---|---|
# | `def add(a, b):` | Define a function named add with two inputs. |
# | `return a + b` | Calculate their sum and send it back. |
# | `print(...)` | Display the returned answer. |
# 
# Python uses `+` for addition, `-` for subtraction, `*` for multiplication and `/` for division.

# %%
def add(a, b):
    return a + b

print(add(5, 3))
print(add(2.5, 1.5))

# %% [markdown]
# **Observe:** `8` and `4.0`. We called Python ourselves. There is no LLM and no tool yet.
# 
# **Try:** change the two inputs. What would you replace `+` with to multiply them?

# %% [markdown]
# ### M2. Install LangChain and import the tool helper
# 
# **PPT checkpoint: slides 9**
# Run this once. If Colab requests a restart, restart and rerun the cells from M1.
# 
# We keep the same LangChain and Groq packages as Module 3. `langchain-core` contains the `tool` helper; `langchain-groq` connects us to Groq's model.

# %%
# Install dependencies with the terminal command above.

# %%
from langchain_core.tools import tool

# %% [markdown]
# **Observe:** the import makes `tool` available. It does not run a calculation or call an LLM.
# 
# `from langchain_core.tools` selects the library module. `import tool` brings its helper into our notebook.

# %% [markdown]
# ### M3. Make the addition tool — read every new symbol
# 
# **PPT checkpoint: slides 9–11**
# We now define a **new name**, `add_numbers`, so the ordinary `add` function above stays unchanged.
# 
# | New piece | Simple meaning |
# |---|---|
# | `@tool` | Apply LangChain's helper to the function below it. This use of `@` is a Python decorator. |
# | `a: float, b: float` | Two number inputs; decimal values are allowed. |
# | `-> float` | Document that the function returns a number. |
# | Triple-quoted sentence | A docstring: explains the purpose so the model can choose this tool. |
# | `return a + b` | The actual Python calculation. |
# 
# `@tool` wraps the function as a LangChain tool. It does **not** execute the calculation. No classes or inheritance are needed.

# %%
@tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers a and b. Use for addition or finding their total."""
    return a + b

print(add_numbers.invoke({"a": 5, "b": 3}))

# %% [markdown]
# **Observe:** `8.0`. `.invoke()` runs the tool with a **dictionary of named inputs**. The keys `"a"` and `"b"` must match the function's input names.
# 
# Calling the ordinary function uses `add(5, 3)`. Calling our decorated tool uses `add_numbers.invoke({"a": 5, "b": 3})`.
# 
# *Roman Urdu: @tool function ko tool banata hai. .invoke us tool ko chalata hai.*

# %% [markdown]
# ### M4. Make the subtraction tool
# 
# **PPT checkpoint: slides 12**
# Only the tool name, purpose and operation change. `a - b` means **subtract b from a**.
# 
# For “Subtract 4 from 15,” we need `a=15`, `b=4`. The input order matters!

# %%
@tool
def subtract_numbers(a: float, b: float) -> float:
    """Subtract b from a. Use for subtraction or finding a minus b."""
    return a - b

print(subtract_numbers.invoke({"a": 15, "b": 4}))

# %% [markdown]
# **Observe:** `11.0`. Swap the input values and try again. You get `-11.0` because `4 - 15` is a different calculation.

# %% [markdown]
# ### M5. Make the multiplication tool
# 
# **PPT checkpoint: slides 13**
# Python uses `*`, not the written × symbol. Predict `6 * 7`.

# %%
@tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers a and b. Use for multiplication or their product."""
    return a * b

print(multiply_numbers.invoke({"a": 6, "b": 7}))

# %% [markdown]
# **Observe:** `42.0`. Try a decimal or a negative number. The model is still not involved: we are testing each tool locally first.

# %% [markdown]
# ### M6. Make the division tool and handle zero
# 
# **PPT checkpoint: slides 14**
# `a / b` means **divide a by b**. Division by zero has no valid result, so our function returns a clear message.
# 
# | New piece | Meaning |
# |---|---|
# | `if b == 0:` | Check whether the second number equals zero. `==` compares; `=` assigns. |
# | First `return` | Stop here and report the invalid operation. |
# | `str(a / b)` | Calculate the quotient, then convert it to text. |
# | `-> str` | This tool returns text, either the quotient or an error message. |
# 
# Tools may return numbers or text. Our division tool uses text so both outcomes have the same return type.

# %%
@tool
def divide_numbers(a: float, b: float) -> str:
    """Divide a by b. Use for division. Report an error if b is zero."""
    if b == 0:
        return "Cannot divide by zero. Please choose a non-zero divisor."
    return str(a / b)

print(divide_numbers.invoke({"a": 20, "b": 4}))
print(divide_numbers.invoke({"a": 20, "b": 0}))

# %% [markdown]
# **Observe:** `5.0`, followed by the division-by-zero message. Do not replace that message with a made-up number.

# %% [markdown]
# ### M7. See the tool menu the model will receive
# 
# **PPT checkpoint: slides 15**
# Each tool has a **name**, a **description** and named **input requirements**. LangChain builds those requirements from the type hints.
# 
# `[ ... ]` creates a list. The `for` loop visits each item in that list. Here it prints the four tools' information.

# %%
math_tools = [
    add_numbers,
    subtract_numbers,
    multiply_numbers,
    divide_numbers,
]

for maths_tool in math_tools:
    print("Name:", maths_tool.name)
    print("Purpose:", maths_tool.description)
    print("Inputs:", maths_tool.args)
    print()

# %% [markdown]
# **Observe:** all four tools require `a` and `b`, both numbers. Clear names and docstrings help the LLM choose the operation. The model receives these definitions; it does not receive or execute our function bodies.

# %% [markdown]
# ### M8. Connect Groq privately
# 
# **PPT checkpoint: slides 16**
# The calculations above did not need a key. The next steps ask the LLM to choose tools, so now we need the key.
# 
# Create a `.env` file in the opened notebook folder containing `GROQ_API_KEY=your_private_key`. Keep `.env` out of GitHub. The next cell reads it or asks for hidden input. Never paste a key into the code or print it.

# %%
import os
from getpass import getpass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")
if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass("Enter your private Groq key: ").strip()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("A Groq key is required for live model calls.")
print("Key is ready. Its value stays hidden.")

# %% [markdown]
# We keep Module 3's Groq model. Three imports do three jobs:
# 
# | Import | Job |
# |---|---|
# | `ChatGroq` | Connects to the Groq-hosted LLM. |
# | `ChatPromptTemplate` | Prepares system instructions and the user question. |
# | `ToolMessage` | Sends a Python tool result back with its matching request ID. |
# 
# Creating `llm` sets up the connection. It does not send a question yet.

# %%
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage

MODEL_NAME = "openai/gpt-oss-20b"
llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0,
    timeout=60,
    max_retries=1,
)

# %% [markdown]
# ### M9. Offer all four tools and give the model rules
# 
# **PPT checkpoint: slides 17–18**
# `bind_tools(math_tools)` tells the model what is available. **It does not run any tool.** The model chooses the tool and input values when it receives a question.
# 
# The system prompt asks for a tool on maths questions and asks for missing numbers. `{question}` is the familiar Module 3 placeholder.
# 
# Start with **one operation and two numbers**. This beginner app handles one batch of requests. Dependent multi-step calculations would need another request/execution round, which is outside this warm-up.

# %%
math_llm = llm.bind_tools(math_tools)

math_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a beginner-friendly maths assistant. "
     "Use the available maths tools for calculations. "
     "Start with one operation and two numbers. "
     "Ask for missing numbers or an unclear operation. "
     "For subtraction, a is the starting number and b is subtracted from it. "
     "For division, divide a by b. "
     "After a tool result, explain only the returned result. "
     "Report division by zero honestly. Answer general explanations directly."),
    ("human", "{question}"),
])

# %% [markdown]
# **Predict:** for “Multiply 6 by 7,” which tool should the model request? What values should `a` and `b` have?
# 
# We did not write keyword checks such as `if "multiply" in question`. The LLM will interpret the wording and choose from the four tool definitions.

# %% [markdown]
# ### M10. Let the user type a question — inspect the first LLM response
# 
# **PPT checkpoint: slides 19–20**
# This is our **first live LLM call**. Type a simple calculation, for example:
# 
# - Add 12 and 8.
# - Subtract 4 from 15.
# - Multiply 6 by 7.
# - Divide 20 by 4.
# 
# `input()` lets the user type. `.strip()` removes extra spaces. `or` uses the example if the input is blank.
# 
# We keep the **full AI message** rather than using `StrOutputParser`, because we need its `.tool_calls`.

# %%
math_question = input("Ask a maths question: ").strip()
math_question = math_question or "Subtract 4 from 15."

math_messages = math_prompt.invoke({"question": math_question}).to_messages()
math_request = math_llm.invoke(math_messages)

print("Text:", math_request.content)
print("Requested tools:", math_request.tool_calls)

# %% [markdown]
# **Observe:** for the default subtraction question, expect a call with:
# 
# ```python
# {"name": "subtract_numbers", "args": {"a": 15, "b": 4}, "id": "..."}
# ```
# 
# This is an **illustration**, not a response to copy into the live conversation. The real ID will differ.
# 
# `name` selects the function. `args` supplies the two numbers. `id` labels the request. Empty `.content` can be normal during a tool request.
# 
# **Important:** the model has requested a calculation. Our Python application has not executed that request yet!
# 
# If there is no call, inspect the prompt and question. Automatic choice may produce a direct answer or ask for missing input. For a known complete question, an optional teaching demonstration can use `llm.bind_tools(math_tools, tool_choice="subtract_numbers")`; keep automatic choice in the final app.

# %% [markdown]
# ### M11. Write the Python function that selects the requested tool
# 
# **PPT checkpoint: slides 21–22**
# Our application accepts only the four names we defined.
# 
# | Code | Meaning |
# |---|---|
# | `call["name"]` | Read the requested tool name. |
# | `call["args"]` | Read the dictionary of supplied input values. |
# | `if` / `elif` / `else` | Choose the matching branch; `elif` means “otherwise, if”. |
# | `.invoke(inputs)` | Run the selected Python tool with those values. |
# | `try` / `except` | Attempt the call; give a clear result if its inputs are invalid. |
# | `str(result)` | Make a number into text so it can be sent as a ToolMessage. |
# 
# This checks the **name already chosen by the LLM**. It does not choose an operation by reading the user's sentence. We never run model-generated Python code.

# %%
def execute_math_call(call):
    tool_name = call["name"]
    inputs = call["args"]

    try:
        if tool_name == "add_numbers":
            result = add_numbers.invoke(inputs)
        elif tool_name == "subtract_numbers":
            result = subtract_numbers.invoke(inputs)
        elif tool_name == "multiply_numbers":
            result = multiply_numbers.invoke(inputs)
        elif tool_name == "divide_numbers":
            result = divide_numbers.invoke(inputs)
        else:
            result = "Tool unavailable. Only our four maths tools are allowed."
    except Exception:
        result = "Tool error. Please provide two valid numbers named a and b."

    return str(result)

# %% [markdown]
# Test this helper locally with a saved example. This is a teaching example; do not send its made-up ID to the LLM.

# %%
sample_math_call = {
    "name": "multiply_numbers",
    "args": {"a": 6, "b": 7},
    "id": "classroom_example",
}
print(execute_math_call(sample_math_call))

# %% [markdown]
# **Observe:** `42.0`. Try changing `name` to `add_numbers`. The same inputs now produce `13.0`. Python executes whichever **allowed name** the request contains.

# %% [markdown]
# ### M12. Execute the real LLM request and return its result
# 
# **PPT checkpoint: slides 23**
# `messages.append(...)` adds a message to the list. `for` visits every requested call.
# 
# Keep the original AI request first. For each call, execute the tool, print its trace, and append a `ToolMessage` with the **same ID**.
# 
# The ID answers: **“Which request is this result for?”** Never replace it with the tool name or a made-up ID.

# %%
if math_request.invalid_tool_calls:
    raise ValueError("Invalid tool request. Retry M10 with a simpler question.")

# Rebuild from the question used in M10, so rerunning does not duplicate results.
math_messages = math_prompt.invoke({"question": math_question}).to_messages()
math_messages.append(math_request)

for call in math_request.tool_calls:
    result = execute_math_call(call)
    print("Tool chosen by LLM:", call["name"])
    print("Inputs:", call["args"])
    print("Python result:", result)
    math_messages.append(ToolMessage(
        content=result,
        tool_call_id=call["id"],
    ))

# %% [markdown]
# **Observe:** for “Subtract 4 from 15,” the trace should show `subtract_numbers`, the inputs 15 and 4, and Python result `11.0`.
# 
# If the model requested several independent calls, every request gets a matching result. If it made no tool request, the loop runs zero times.

# %% [markdown]
# ### M13. Let the model explain the returned answer
# 
# **PPT checkpoint: slides 24**
# The original `llm` has no tools attached. This second call reads our returned result and produces the final explanation.
# 
# If no tool was requested, display the first answer instead.

# %%
if math_request.tool_calls:
    math_answer = llm.invoke(math_messages)
    print("Assistant:", math_answer.content)
else:
    print("Assistant:", math_request.content)

# %% [markdown]
# **Observe:** wording may vary, but the subtraction answer should explain that 15 minus 4 is 11.
# 
# **Trace the whole flow:** user question → LLM tool request → Python calculation → matching tool result → LLM explanation.
# 
# *Roman Urdu: Model ne tool choose kiya. Python ne hisaab kiya. Result wapas model ko diya, phir model ne user ko samjhaya.*

# %% [markdown]
# ### M14. Collect the steps into our complete maths app
# 
# **PPT checkpoint: slides 25–26**
# All actions below have already appeared. We reuse `execute_math_call` rather than copying the four selection branches again.
# 
# Each question begins a fresh conversation. The app accepts one batch of tool requests and then asks for the final explanation.

# %%
def ask_math_assistant(question):
    # 1. Prepare the user question and system rules.
    messages = math_prompt.invoke({"question": question}).to_messages()

    # 2. Let the LLM request an operation and its inputs.
    request = math_llm.invoke(messages)
    if request.invalid_tool_calls:
        return "Invalid tool request. Please retry with a simpler question."
    if not request.tool_calls:
        return request.content or "No answer returned. Please retry."

    # 3. Keep the request before adding matching Python results.
    messages.append(request)
    for call in request.tool_calls:
        result = execute_math_call(call)
        print("Tool chosen by LLM:", call["name"])
        print("Inputs:", call["args"])
        print("Python result:", result)
        messages.append(ToolMessage(
            content=result,
            tool_call_id=call["id"],
        ))

    # 4. Ask the original model to explain the result.
    answer = llm.invoke(messages)
    return answer.content or "No final answer returned. Please retry."

# %% [markdown]
# ### M15. Run your app with user input
# 
# **PPT checkpoint: slides 27**
# Run this cell again for each new question. Watch the tool name, input values and Python result before reading the final answer.

# %%
question = input("Ask your maths assistant: ").strip()
question = question or "Multiply 6 by 7."

try:
    answer = ask_math_assistant(question)
    print("Assistant:", answer)
except Exception as error:
    print("Model call failed:", type(error).__name__)
    print("Check your key, internet connection, model access and Groq quota.")

# %% [markdown]
# ### M16. Check all four operations before moving on
# 
# **PPT checkpoint: slides 28–29**
# Try one question at a time in M15. These are expected behaviors to verify, not guaranteed model outputs.
# 
# | User question | Expected tool / behavior | Python result to check |
# |---|---|---|
# | Add 12 and 8. | `add_numbers(a=12, b=8)` | 20 |
# | Subtract 4 from 15. | `subtract_numbers(a=15, b=4)` | 11 |
# | Multiply 6 by 7. | `multiply_numbers(a=6, b=7)` | 42 |
# | Divide 20 by 4. | `divide_numbers(a=20, b=4)` | 5 |
# | Add 2.5 and 1.5. | `add_numbers` with decimals | 4 |
# | Divide 20 by 0. | `divide_numbers` | Honest division-by-zero message |
# | Add 5. | Ask for the second number | No invented input |
# | What is multiplication? | Explain directly | A calculation tool may be unnecessary |
# 
# **Mini challenge:** say “What is the total of 9 and 6?” Can the LLM recognize addition even without the word “add”?
# 
# **Before continuing, explain:**
# 1. What does `@tool` do? Does it execute the calculation?
# 2. Does `bind_tools` run Python?
# 3. Who chooses the operation, and who performs it?
# 4. Why must `tool_call_id` match the request ID?
# 
# **Answers:** `@tool` creates the tool wrapper; it does not run the calculation. `bind_tools` supplies definitions. The LLM requests an operation and inputs; our Python app executes it. The matching ID connects each result to its request.
# 
# ## Part B — Now build the parcel tracking assistant
# You already know the complete tool-calling flow. Now replace **“calculate with two numbers”** with **“look up a saved status using a tracking ID.”**
# 
# | Maths assistant | Parcel assistant |
# |---|---|
# | Four calculation tools | One parcel lookup tool |
# | Inputs `a` and `b` are numbers | Input `tracking_id` is text |
# | Python returns a calculation | Python returns a saved status |
# | Match result to request ID | The same matching rule |
# | LLM explains the returned answer | The same final explanation step |
# 
# The original parcel steps **1–20**, assignment and reference solution continue below. Their imports and setup are repeated so Part B can also be demonstrated on its own.

# %% [markdown]
# ## 1. Our first Python function
# 
# **PPT checkpoint: slides 30–31**
# 
# `def` defines a function. `tracking_id` is its input. `return` sends text back to the caller.
# 
# *Roman Urdu: Function aik kaam karta hai. Input leta hai aur result wapas deta hai.*

# %%
def first_parcel_function(tracking_id):
    return "Out for delivery in Multan."

print(first_parcel_function("PK101"))
print(first_parcel_function("PK102"))

# %% [markdown]
# **Observe:** Both calls return the same sentence. **Challenge:** PK102 should have a different status. We need a lookup using its ID, rather than one fixed sentence.

# %% [markdown]
# ## 2. Save three sample records
# 
# **PPT checkpoint: slides 32**
# 
# A **dictionary** keeps named values. Each tracking number is a key. Its status is the value.

# %%
PARCELS = {
    "PK101": "Out for delivery in Multan.",
    "PK102": "In transit to Karachi.",
    "PK103": "Delivered in Lahore.",
}

print(PARCELS["PK101"])
print(PARCELS["PK102"])

# %% [markdown]
# **Observe:** PK101 and PK102 now give different statuses. Try reading PK103. These sample records act like a tiny database for our classroom.

# %% [markdown]
# ## 3. Handle a record that does not exist
# 
# **PPT checkpoint: slides 32–33**
# 
# `dictionary.get(key, fallback)` looks for a key. If it is missing, it returns the fallback text.
# 
# This lets our app honestly report an unknown parcel.

# %%
print(PARCELS.get("PK101", "Tracking number not found."))
print(PARCELS.get("PK999", "Tracking number not found."))

# %% [markdown]
# **Observe:** The first output is a saved status. The second is `Tracking number not found.` Do not invent a status for an unknown ID.

# %% [markdown]
# ## 4. Build and test the real lookup function
# 
# **PPT checkpoint: slides 33**
# 
# `.strip()` removes spaces at the ends. `.upper()` converts letters to capitals. Then `.get()` reads the matching record.
# 
# Each dot means “use this ready-made command.”

# %%
def lookup_parcel(tracking_id):
    clean_id = tracking_id.strip().upper()
    return PARCELS.get(clean_id, "Tracking number not found in the classroom data.")

print(lookup_parcel("PK101"))
print(lookup_parcel(" pk102 "))
print(lookup_parcel("PK999"))

# %% [markdown]
# **Observe:** You get the PK101 status, the PK102 status, and an honest not-found message. No LLM has run yet.
# 
# **Pause:** explain which line reads the data and which line handles spaces/capital letters.

# %% [markdown]
# ### Install LangChain packages
# This notebook uses `langchain-core` and `langchain-groq`, matching the Module 3 imports.
# Run this cell once. If the notebook requests a restart, restart and rerun Steps 1–4 before continuing.
# 
# If you completed Part A, these versions are already installed. You may skip this install cell in the same session. Rerun it when starting Part B in a fresh runtime.

# %%
# Install dependencies with the terminal command above.

# %% [markdown]
# ## 5. Import the tool helper
# 
# **PPT checkpoint: slides 34**
# 
# `from ... import ...` brings a library helper into this notebook.
# 
# We use `langchain_core.tools` because Module 3 already used `langchain-core`. It belongs to the LangChain ecosystem.

# %%
from langchain_core.tools import tool

# %% [markdown]
# **Observe:** `tool` is now available. We will use it on the next function. Importing it does not call the LLM or run a tool.

# %% [markdown]
# ## 6. Make our first LangChain tool
# 
# **PPT checkpoint: slides 35–37**
# 
# Read these four new pieces before running:
# 
# - `@tool`: applies the helper to the function below it. This use of `@` is called a **decorator**.
# - `tracking_id: str`: the tool expects text. `str` means a string.
# - `-> str`: the tool returns text.
# - The triple-quoted sentence: a **docstring** describing the tool to the model.
# 
# Our tool reuses the ordinary function we already tested. No OOP class is required.

# %%
@tool
def get_parcel_status(tracking_id: str) -> str:
    """Look up a parcel status using its tracking ID. Use this for parcel tracking questions."""
    return lookup_parcel(tracking_id)

# %% [markdown]
# **Observe:** We have defined a tool, but we have not run it.
# 
# **How @tool works:** it is equivalent to writing `get_parcel_status = tool(get_parcel_status)` after defining a function. Do not run that extra wrapper line here because our function is already decorated.

# %% [markdown]
# ## 7. Run the tool ourselves
# 
# **PPT checkpoint: slides 38**
# 
# After `@tool`, this name refers to a LangChain tool. We run it with `.invoke()` and a dictionary of named inputs.
# 
# The ordinary function still uses `lookup_parcel("PK101")`.

# %%
tool_inputs = {"tracking_id": "PK101"}
result = get_parcel_status.invoke(tool_inputs)
print(result)

# Change the input and run again.
print(get_parcel_status.invoke({"tracking_id": "PK103"}))

# %% [markdown]
# **Observe:** Outputs: `Out for delivery in Multan.` and `Delivered in Lahore.` This still runs locally with no LLM call.

# %% [markdown]
# ## 8. Inspect what the model will learn about our tool
# 
# **PPT checkpoint: slides 39**
# 
# A **schema** describes the input fields and their types. LangChain derives it from the function definition. We do not manually write a schema or a Pydantic class.

# %%
print("Name:", get_parcel_status.name)
print("Description:", get_parcel_status.description)
print("Inputs:", get_parcel_status.args)

# %% [markdown]
# **Observe:** Name: `get_parcel_status`. One input: `tracking_id`, whose type is string. The model receives a tool definition, not the function body or the entire PARCELS dictionary.
# 
# **Mini challenge:** improve the docstring so it clearly says when to use the tool. Rerun Step 6 and then Step 8.

# %% [markdown]
# ### Private Groq key for VS Code
# Create a `.env` file in the opened notebook folder containing `GROQ_API_KEY=your_private_key`.
# Keep `.env` out of GitHub. The hidden-input fallback works if you prefer not to use a file.

# %%
import os
from getpass import getpass
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path.cwd() / ".env")
if not os.getenv("GROQ_API_KEY"):
    os.environ["GROQ_API_KEY"] = getpass("Enter your private Groq key: ").strip()
if not os.getenv("GROQ_API_KEY"):
    raise ValueError("A Groq key is required for live model calls.")
print("Key is ready. Its value stays hidden.")

# %% [markdown]
# ## 9. Reconnect the same Groq model
# 
# **PPT checkpoint: slides 40**
# 
# We now need two familiar Module 3 imports and one new message helper.
# 
# | Import | Job |
# |---|---|
# | `ChatGroq` | Calls the model through Groq. |
# | `ChatPromptTemplate` | Creates messages using input variables. |
# | `ToolMessage` | Carries a function result back to the model. |

# %%
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import ToolMessage

MODEL_NAME = "openai/gpt-oss-20b"
llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0,
    timeout=60,
    max_retries=1,
)

# %% [markdown]
# **Observe:** We retain the latest Module 3 model, hosted by Groq. Model availability and account permissions can change. This cell creates settings, but does not send a question yet.

# %% [markdown]
# ## 10. Let the model see our tool
# 
# **PPT checkpoint: slides 41**
# 
# `bind_tools()` attaches available tool definitions. The model can use the name, purpose and input types to request a tool.
# 
# **It does not execute the Python function.**

# %%
llm_with_tools = llm.bind_tools([get_parcel_status])

# %% [markdown]
# **Observe:** Square brackets make a list containing our one tool. The model can request it, answer directly, or ask for missing information.
# 
# **Module 3 connection:** a `RunnableLambda` runs where we place it in a chain. Here the model decides whether to request a tool.

# %% [markdown]
# ## 11. Reuse our Module 3 prompt template
# 
# **PPT checkpoint: slides 42**
# 
# The system message sets rules. The `{question}` placeholder receives the user question.
# 
# The model must use the tool for saved parcel status and must not invent a delivery time.

# %%
parcel_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a parcel assistant for fictional classroom records. "
     "Use get_parcel_status for status questions. Ask for the tracking ID if missing. "
     "Never invent a status or delivery time. Answer general explanations directly. "
     "After a tool result, explain it in simple English using only the returned facts."),
    ("human", "{question}"),
])

prepared_prompt = parcel_prompt.invoke({"question": "Where is my parcel PK101?"})
messages = prepared_prompt.to_messages()
print(prepared_prompt.to_string())

# %% [markdown]
# **Observe:** This prepares messages locally. `to_messages()` gives the model a list of messages.
# 
# We keep the AI message after a tool request. We will **not** put `StrOutputParser()` before examining tool calls.

# %% [markdown]
# ## 12. Get the first live tool request
# 
# **PPT checkpoint: slides 43–44**
# 
# This is the first live model call in our parcel project, following the maths warm-up. The model reads the question and may request our tool.
# 
# We keep a small chain just like Module 3, but without a text parser: `parcel_prompt | llm_with_tools`.

# %%
request_chain = parcel_prompt | llm_with_tools
ai_request = request_chain.invoke({"question": "Where is my parcel PK101?"})

print("Text:", ai_request.content)
print("Tool calls:", ai_request.tool_calls)

# %% [markdown]
# **Observe:** Expected request: tool `get_parcel_status`, argument `tracking_id="PK101"`. The call ID and wording can vary. Empty `.content` is normal if a tool request exists.
# 
# **If it answers without requesting a tool:** check the prompt and tool description. For an optional teaching demonstration, bind with `tool_choice="get_parcel_status"` and rerun this known-ID question. Keep automatic choice for the final app.

# %% [markdown]
# ## 13. Read name, args and id
# 
# **PPT checkpoint: slides 45**
# 
# A tool call is a dictionary with `name`, `args` and `id`. In LangChain, `args` is already a Python dictionary.
# 
# The saved example below is **synthetic teaching data**, not a live response.

# %%
example_call = {
    "name": "get_parcel_status",
    "args": {"tracking_id": "PK101"},
    "id": "example_call_1",
}

print("Function:", example_call["name"])
print("Inputs:", example_call["args"])
print("Request label:", example_call["id"])

# Inspect the real call only if the list has an item.
if ai_request.tool_calls:
    first_call = ai_request.tool_calls[0]
    print("Real call:", first_call)
else:
    print("The model returned text or asked for more information.")

# %% [markdown]
# **Observe:** `name` selects the function. `args` supplies the tracking ID. `id` labels this request. `[0]` reads the first item of a list. The `if` avoids reading from an empty list.

# %% [markdown]
# ## 14. Execute a saved request ourselves
# 
# **PPT checkpoint: slides 46–47**
# 
# The request is only instructions. Our Python app must run the tool. Use the same `.invoke()` you tested in Step 7.

# %%
example_result = get_parcel_status.invoke(example_call["args"])
print(example_result)

example_message = ToolMessage(
    content=example_result,
    tool_call_id=example_call["id"],
)
print("Result text:", example_message.content)
print("Matching ID:", example_message.tool_call_id)

# %% [markdown]
# **Observe:** The status comes from Python. `ToolMessage` packages that status with the matching request ID. This saved example is for learning only; do not append it to the live conversation.

# %% [markdown]
# ## 15. Execute the real request and prepare its response
# 
# **PPT checkpoint: slides 48**
# 
# We now apply the same steps to the actual LLM request.
# 
# A `for` loop visits each call in the list. A response may request more than one call. `append()` adds an item to the message list.
# 
# `try` runs a local tool that might fail. `except` gives a simple error result. Unknown tool names cannot execute.

# %%
if ai_request.invalid_tool_calls:
    raise ValueError("Invalid tool request. Retry Step 12 with a simpler question.")

# Rebuild this list from the exact question used for ai_request.
# This makes rerunning this cell safe: old results do not accumulate.
messages = parcel_prompt.invoke({"question": "Where is my parcel PK101?"}).to_messages()
messages.append(ai_request)

for call in ai_request.tool_calls:
    try:
        if call["name"] != "get_parcel_status":
            result = "Tool unavailable. Only get_parcel_status is allowed."
        else:
            result = get_parcel_status.invoke(call["args"])
    except Exception:
        result = "Tool error. Please provide a valid tracking ID as text."

    print("Python result:", result)
    messages.append(ToolMessage(
        content=result,
        tool_call_id=call["id"],
    ))

# %% [markdown]
# **Observe:** Message order: original user messages, original AI tool request, then a matching result for every requested call. Preserve each request ID.
# 
# *Roman Urdu: Model request karta hai. Python tool chalata hai. Har result apni request ke ID ke saath wapas jata hai.*

# %% [markdown]
# ## 16. Ask for the final explanation
# 
# **PPT checkpoint: slides 49–50**
# 
# If the first call requested a tool, the second model call reads the returned result and explains it. If there was no tool call, we display the original text.

# %%
if ai_request.tool_calls:
    final_answer = llm.invoke(messages)
    print(final_answer.content)
else:
    print(ai_request.content)

# %% [markdown]
# **Observe:** The response should use the saved status for PK101 and avoid inventing a delivery time. Our simple app uses an unbound model for the final explanation, completing one batch of requests. Usually this path needs two API calls and local function execution.

# %% [markdown]
# ## 17. Assemble our complete app
# 
# **PPT checkpoint: slides 51–52**
# 
# Every important action below has already appeared in a previous step. We collect them inside an ordinary function.
# 
# Each question begins a fresh conversation. The app handles one request batch, then asks for a final answer. We are not building an autonomous agent loop in this class.

# %%
def ask_parcel_assistant(question):
    # 1. Reuse our Module 3 prompt template.
    messages = parcel_prompt.invoke({"question": question}).to_messages()

    # 2. Ask the model whether it needs our tool.
    request = llm_with_tools.invoke(messages)
    if request.invalid_tool_calls:
        return "The model returned an invalid tool request. Please retry."
    if not request.tool_calls:
        # A general question or missing tracking ID may need no tool.
        return request.content or "No answer returned. Please retry."

    # 3. Preserve the AI request before adding its results.
    messages.append(request)
    for call in request.tool_calls:
        print("Tool:", call["name"])
        print("Inputs:", call["args"])
        try:
            # This beginner app permits only our one registered tool.
            if call["name"] != "get_parcel_status":
                result = "Tool unavailable. Only get_parcel_status is allowed."
            else:
                result = get_parcel_status.invoke(call["args"])
        except Exception:
            # A malformed input should produce an honest error result.
            result = "Tool error. Please provide a valid tracking ID as text."
        print("Python result:", result)

        # 4. Match each result to the request that produced it.
        messages.append(ToolMessage(
            content=result,
            tool_call_id=call["id"],
        ))

    # 5. Ask the original model to explain the returned results.
    # No tools are attached here, so this completes one request batch.
    answer = llm.invoke(messages)
    return answer.content or "No final answer returned. Please retry."

# %% [markdown]
# **Observe:** Read the numbered comments. Trace a question through preparation, request, execution, result message and final answer. No custom class is introduced.

# %% [markdown]
# ## 18. Run the app and inspect its trace
# 
# **PPT checkpoint: slides 53**
# 
# Change one question at a time. A trace shows which tool the model requested, its inputs, and the result Python returned.
# 
# Try the fixed question before enabling `input()`.

# %%
question = "Please track PK102."
# question = input("Ask the parcel assistant: ").strip()

try:
    answer = ask_parcel_assistant(question)
    print("Assistant:", answer)
except Exception as error:
    print("Model request failed:", type(error).__name__)
    print("Check your private Groq key, internet, model access, and quota.")

# %% [markdown]
# **Observe:** The tool should return `In transit to Karachi.` The final answer wording may vary. This is now a usable notebook application accepting natural-language questions.

# %% [markdown]
# ## 19. Test whether your app behaves correctly
# **PPT checkpoint: slides 54–55**
# 
# Change `question` in Step 18 and run one question at a time.
# 
# | Question | What to check |
# |---|---|
# | Where is PK101? | Tool gets PK101 and returns the saved Multan status. |
# | Track pk103 please. | The lookup handles lower-case letters and returns Delivered in Lahore. |
# | Where is PK999? | The tool reports the ID is not in our classroom data. |
# | Where is my parcel? | The model asks for a tracking ID. It should not invent one. |
# | What is a tracking number? | A direct explanation is appropriate. |
# | Track PK101 and PK102. | If multiple calls appear, each gets its own matching ToolMessage. |
# 
# Expected behavior is something to **evaluate**, not a guarantee about the model's decisions.
# For each question record: **tool used? inputs? function result? final answer supported?**
# 
# ### Your checkpoint
# Explain these without looking:
# 1. Which import creates tools?
# 2. What does `@tool` do?
# 3. What does `bind_tools()` do?
# 4. Who runs the Python function?
# 5. What connects a result to a request?
# 
# Answers: `from langchain_core.tools import tool`; wraps the function; attaches tool definitions; our Python application; matching `tool_call_id`.

# %% [markdown]
# ## 20. Class assignment: a book availability assistant
# **PPT checkpoint: slides 56–57**
# 
# A student asks: **“Is Python Basics available?”**
# Build one tool called `check_book_availability(book_title: str) -> str`.
# Use this classroom data:
# - Python Basics: Available
# - AI for Beginners: Borrowed
# - Electronics Starter: Available
# 
# ### Your task
# 1. Store the sample book data in a dictionary.
# 2. Build and test an ordinary lookup function.
# 3. Add a clear tool name, docstring, type hint and `@tool`.
# 4. Test `.invoke()` locally before using the model.
# 5. Bind the tool and adapt the system prompt.
# 6. Reuse Steps 17–18 with your new tool and the new allowed name.
# 
# ### Submit evidence
# - Known book: correct saved status.
# - Unknown book: honest not-found message.
# - Missing title: model asks for a title.
# - One printed tool trace showing inputs and local output.
# 
# **No borrowing, purchasing, external database or second tool is required.**
# Try this independently before opening the reference solution below.

# %%
# Assignment starter: run this cell when you begin the assignment.
BOOKS = {
    "python basics": "Available",
    "ai for beginners": "Borrowed",
    "electronics starter": "Available",
}

# TODO 1: Write an ordinary function that looks up book_title.
# Hint: use book_title.strip().lower() to match these keys.
# TODO 2: Add @tool, a docstring, and text input/output hints.
# TODO 3: Test the tool with .invoke({"book_title": "Python Basics"}).
# TODO 4: Replace the parcel tool in bind_tools().
# TODO 5: Change the prompt rules and allowed tool-name check.
# TODO 6: Run known, unknown, and missing-title questions.

# %% [markdown]
# <details><summary>Reference solution: open only after trying the assignment</summary>
# 
# ```python
# @tool
# def check_book_availability(book_title: str) -> str:
#     """Check whether a book is available in the fictional classroom library."""
#     title = book_title.strip().lower()
#     return BOOKS.get(title, "Book not found in the classroom library.")
# 
# # Check the function locally before calling the model.
# print(check_book_availability.invoke({"book_title": "Python Basics"}))
# 
# book_model = llm.bind_tools([check_book_availability])
# book_prompt = ChatPromptTemplate.from_messages([
#     ("system", "You are a classroom library assistant. Use check_book_availability "
#      "for availability questions. Ask for a missing title. Never invent availability. "
#      "Explain tool results in simple English. Answer general questions directly."),
#     ("human", "{question}"),
# ])
# 
# def ask_book_assistant(question):
#     messages = book_prompt.invoke({"question": question}).to_messages()
#     request = book_model.invoke(messages)
#     if request.invalid_tool_calls:
#         return "Invalid tool request. Please retry."
#     if not request.tool_calls:
#         return request.content or "No answer returned. Please retry."
#     messages.append(request)
#     for call in request.tool_calls:
#         try:
#             if call["name"] != "check_book_availability":
#                 result = "Tool unavailable."
#             else:
#                 result = check_book_availability.invoke(call["args"])
#         except Exception:
#             result = "Please provide a valid book title as text."
#         print("Book inputs:", call["args"])
#         print("Book result:", result)
#         messages.append(ToolMessage(content=result, tool_call_id=call["id"]))
#     return llm.invoke(messages).content
# 
# print(ask_book_assistant("Is Python Basics available?"))
# ```
# </details>

# %% [markdown]
# ## Troubleshooting and reuse
# **PPT checkpoint: slide 58**
# 
# | Symptom | What to do |
# |---|---|
# | ModuleNotFoundError | Run the install cell in the selected notebook kernel. Restart and rerun definitions if requested. |
# | 401 / authentication error | Check the private Groq key. Never print it. |
# | 429 / rate limit | Wait, reduce repeated questions, and check account quota. |
# | Model unavailable | Check the Groq catalog and project permissions. |
# | Empty response text | Inspect `.tool_calls`. A request can have empty `.content`. |
# | No tool call | The model may explain or ask for missing information. Check the docstring and rules. |
# | Invalid tool call / 400 | Simplify the question and confirm the selected model supports tool calling. |
# | Tool-result protocol error | Keep the original AI request and include a matching result for every call ID. |
# 
# ### Your reusable recipe
# Write a normal function. Test it. Describe its inputs and purpose. Add `@tool`. Bind it. Inspect requests. Run allowed functions. Send matching results. Explain the output.
# 
# Tools connect an LLM to application data and code. They can still receive wrong inputs or encounter unavailable data, so test both ordinary and unusual questions.
# For real actions such as sending an email, changing a record, or taking payment, the application must add the relevant authorization and confirmation.
# Never execute arbitrary model-generated code with `eval()` or `exec()`.
# 
# ### Sources
# - [LangChain tools](https://docs.langchain.com/oss/python/langchain/tools)
# - [LangChain models and tool calls](https://docs.langchain.com/oss/python/langchain/models)
# - [ChatGroq integration](https://docs.langchain.com/oss/python/integrations/chat/groq)
# - [Groq tool use](https://console.groq.com/docs/tool-use/overview)
# - [Groq-hosted GPT OSS 20B](https://console.groq.com/docs/model/openai/gpt-oss-20b)
# 
# **Prepared by Engr Usman Hasan**
