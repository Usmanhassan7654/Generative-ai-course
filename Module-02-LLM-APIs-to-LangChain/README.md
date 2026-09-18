# Module 2 — From LLM APIs to LangChain
## Beginner Classroom Setup — Windows + VS Code + Python

This classroom project teaches this progression:

```text
Python
  ↓
Call Gemini directly
  ↓
Call Groq directly
  ↓
Notice the provider-specific repetition
  ↓
Introduce LangChain
  ↓
Use a more consistent interface for different LLMs
  ↓
Practice normal prompts
  ↓
Practice fixed/static prompts and one reusable template
  ↓
Think about PROMPT ENGINEERING
```

> **Important naming note:** This project uses **Groq** (`groq.com`), the LLM inference/API platform. **Groq is not Grok.** Grok is associated with xAI.

---

# 1. Install Python on Windows

You asked for a Python **3.8+** setup. However, the current 2026 LangChain integrations used in this project require **Python 3.10 or newer**.

For this classroom pack, install **Python 3.10+**; **Python 3.12** is a good classroom choice. This prevents package-installation errors with current `langchain-groq` and `langchain-google-genai`.

## Step 1 — Download Python

Open:

https://www.python.org/downloads/windows/

Download the latest stable Windows installer.

## Step 2 — Run the installer

On the first installation screen, make sure you check:

```text
☑ Add python.exe to PATH
```

Then click **Install Now**.

## Step 3 — Verify Python

Open **Command Prompt** or **PowerShell** and run:

```powershell
python --version
```

You should see something similar to:

```text
Python 3.x.x
```

Also check `pip`:

```powershell
pip --version
```

If `python` is not recognized, close and reopen the terminal first. If it still does not work, reinstall Python and make sure **Add Python to PATH** is selected.

---

# 2. Install Visual Studio Code

Download VS Code from:

https://code.visualstudio.com/

After opening VS Code, install these extensions from the **Extensions** panel:

1. **Python** — by Microsoft
2. **Jupyter** — by Microsoft

These extensions let VS Code run Python files and `.ipynb` notebooks.

---

# 3. Open the project folder in VS Code

In VS Code:

```text
File → Open Folder → Module_2_LLM_APIs_to_LangChain_VSCode
```

Open a terminal:

```text
Terminal → New Terminal
```

---

# 4. Create a Python virtual environment

A **virtual environment** is an isolated Python workspace for one project.

Think of it like giving every project its own toolbox.

Without virtual environments:

```text
Computer Python
├── Project A packages
├── Project B packages
└── Project C packages
```

With virtual environments:

```text
Project A → its own packages
Project B → its own packages
Project C → its own packages
```

## Create the environment

Run:

```powershell
python -m venv .venv
```

What does it mean?

- `python` → run Python
- `-m` → run a Python module
- `venv` → Python's virtual-environment module
- `.venv` → the folder name we want to create

---

# 5. Activate the virtual environment

## PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## Command Prompt (CMD)

```cmd
.venv\Scripts\activate.bat
```

When activation works, you should see something like:

```text
(.venv) C:\...\Module_2_LLM_APIs_to_LangChain_VSCode>
```

## If PowerShell blocks activation

Use Command Prompt and run:

```cmd
.venv\Scripts\activate.bat
```

## Deactivate later

```powershell
deactivate
```

---

# 6. Install the required libraries

Make sure `(.venv)` is visible in the terminal.

Upgrade pip:

```powershell
python -m pip install --upgrade pip
```

Install the libraries:

```powershell
pip install -r requirements.txt
```

The requirements include:

- `python-dotenv` → loads values from `.env`
- `google-genai` → Google's official Gemini Python SDK
- `groq` → Groq's official Python SDK
- `langchain` → LangChain framework
- `langchain-groq` → LangChain integration for Groq
- `langchain-google-genai` → LangChain integration for Gemini
- `ipykernel` → lets VS Code run this notebook from `.venv`

---

# 7. Tell VS Code to use `.venv`

Open:

```text
Module_2_LLM_APIs_to_LangChain.ipynb
```

At the top-right, click:

```text
Select Kernel
```

Choose the Python interpreter inside `.venv`.

It may look like:

```text
Python 3.x.x ('.venv')
```

---

# 8. Create your API keys

This lesson uses provider APIs under their available free/developer-tier limits. Limits can change, so check the provider dashboards when needed.

## Gemini API key

Create a key from Google AI Studio:

https://aistudio.google.com/

## Groq API key

Create a key from Groq Console:

https://console.groq.com/

> Never share API keys in screenshots, GitHub repositories, WhatsApp groups, assignments, or public notebooks.

---

# 9. Store API keys inside `.env`

Open the `.env` file.

It contains:

```env
GEMINI_API_KEY=your_gemini_api_key_here
GROQ_API_KEY=your_groq_api_key_here

GEMINI_MODEL=gemini-3.8-flash
GROQ_MODEL=openai/gpt-oss-20b
```

Replace only the placeholder values:

```env
GEMINI_API_KEY=PASTE_YOUR_REAL_KEY_HERE
GROQ_API_KEY=PASTE_YOUR_REAL_KEY_HERE
```

Do **not** put your real keys directly inside Python code.

Bad:

```python
api_key = "my-secret-real-key"
```

Better:

```python
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
```

---

# 10. Why use `.env`?

Imagine an API key as the key to your house.

You use the key to enter, but you do not paint the key onto the front door.

The `.env` file keeps secrets separate from the application code.

This project also contains `.gitignore`, which tells Git not to upload `.env`.

---

# 11. Stage A — Direct Gemini API

With Google's SDK:

```python
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Explain AI in simple words."
)

print(response.text)
```

Notice that the generated text is accessed using:

```python
response.text
```

---

# 12. Stage B — Direct Groq API

With Groq's SDK:

```python
from groq import Groq

client = Groq(api_key=GROQ_API_KEY)

response = client.chat.completions.create(
    model="openai/gpt-oss-20b",
    messages=[
        {"role": "user", "content": "Explain AI in simple words."}
    ]
)

print(response.choices[0].message.content)
```

Notice the generated text is accessed using:

```python
response.choices[0].message.content
```

---

# 13. The problem we want students to notice

Both programs are conceptually doing:

```text
QUESTION → LLM → ANSWER
```

But the code differs.

| Job | Gemini SDK | Groq SDK |
|---|---|---|
| Import | `from google import genai` | `from groq import Groq` |
| Client | `genai.Client(...)` | `Groq(...)` |
| Generate | `models.generate_content()` | `chat.completions.create()` |
| Input | `contents=` | `messages=` |
| Read text | `response.text` | `response.choices[0].message.content` |

Now imagine supporting Gemini, Groq, OpenAI, Anthropic, Mistral, local models, and more.

Your application starts accumulating different:

- imports
- client objects
- request formats
- response formats
- configuration styles
- provider-specific handling

Direct SDKs are not bad. They are useful, especially when you need a provider's newest specialized feature. But for multi-model applications, a common interface can reduce repetitive integration work.

---

# 14. Enter LangChain

LangChain does **not** replace the LLM.

For today's lesson, think of it as a common layer between your application and different model providers.

```text
                ┌── Gemini
                │
Your Python → LangChain ── Groq
                │
                └── Other providers
```

## Analogy: universal travel adapter

Without an adapter, every electrical socket requires different connection handling.

With a universal adapter, your device interacts through one familiar connection layer.

LangChain plays a similar role at the application level.

---

# 15. Same LangChain-style call for different models

After creating provider objects:

```python
gemini_llm = ChatGoogleGenerativeAI(...)
groq_llm = ChatGroq(...)
```

we can use:

```python
response = gemini_llm.invoke(question)
print(response.content)
```

and:

```python
response = groq_llm.invoke(question)
print(response.content)
```

The underlying provider is different, but the calling pattern becomes much more consistent.

---

# 16. Important LangChain words

## `invoke()`

```python
response = llm.invoke(question)
```

For this class, think of `invoke()` as:

> Send this input through this LangChain component and return one result.

It is the standard synchronous call pattern used by many LangChain components.

## `AIMessage`

A LangChain chat model usually returns a message object such as an `AIMessage`, not only a raw string.

That object can contain the generated answer plus useful metadata.

## `.content`

For the text examples in this lesson:

```python
response.content
```

gives us the generated answer.

## `ChatPromptTemplate`

A prompt template lets us create reusable prompt structures containing variables:

```python
prompt = ChatPromptTemplate.from_template(
    "Explain {topic} to a beginner using one simple analogy."
)
```

`{topic}` can be replaced without rewriting the whole prompt.

## Pipe operator `|`

LangChain lets compatible components be composed:

```python
chain = prompt | llm
```

Read it as:

```text
input
  ↓
prompt template
  ↓
LLM
  ↓
answer
```

Then:

```python
response = chain.invoke({"topic": "API"})
```

---

# 17. Normal prompts vs fixed/static prompts

## Normal prompt

A question can come directly from a user:

```python
question = input("Ask a question: ")
response = llm.invoke(question)
```

## Fixed/static prompt

An application can also contain developer-written instructions:

```python
STATIC_PROMPT = """
You are a beginner-friendly AI teacher.
Explain what an API is.
Use simple English.
Give one everyday analogy.
"""
```

This raises important questions:

- What instructions should we give?
- How specific should we be?
- Does context improve the answer?
- Does asking for a format change the result?
- What happens if the prompt is vague?
- How should system and user instructions be separated?

Those questions lead into the next lesson: **Prompt Engineering**.

---

# 18. Run the notebook

Run the notebook cells from top to bottom.

The lesson story is:

```text
1. Check the environment
2. Load API keys
3. Ask Gemini directly
4. Ask Groq directly
5. Compare provider-specific code
6. Introduce LangChain
7. Ask Gemini through LangChain
8. Ask Groq through LangChain
9. Switch providers with one helper function
10. Practice normal prompts
11. Practice fixed/static prompts
12. Build one reusable prompt template
13. End with a Prompt Engineering experiment
```

---

# 19. Project structure

```text
Module_2_LLM_APIs_to_LangChain_VSCode/
│
├── README.md
├── requirements.txt
├── .env
├── .gitignore
└── Module_2_LLM_APIs_to_LangChain.ipynb
```

After setup, your computer will also contain:

```text
.venv/
```

Do not upload `.venv` to GitHub.

---

# 20. Common errors

## `python is not recognized`

Check:

```powershell
python --version
```

If it fails, Python may not be installed correctly or may not be on PATH.

## `ModuleNotFoundError`

Activate `.venv` and run:

```powershell
pip install -r requirements.txt
```

Also make sure the notebook kernel is using `.venv`.

## API key is `None`

Check `.env` spelling:

```env
GEMINI_API_KEY=...
GROQ_API_KEY=...
```

Restart the notebook kernel and rerun the setup cells.

## Authentication error

Possible causes:

- incorrect key
- copied spaces around the key
- revoked key
- incorrect environment variable name

## Rate-limit error

Free/developer API usage has limits. The exact quotas depend on provider, project, account, and model, and may change.

## Model-not-found error

Cloud model names can change.

This classroom pack currently uses:

```text
Gemini: gemini-3.8-flash
Groq:   openai/gpt-oss-20b
```

If a provider later deprecates a model, update the model name in `.env`.

---

# 21. End-of-class thinking question

Compare these two prompts with the **same model**.

### Prompt A

```text
Explain APIs.
```

### Prompt B

```text
You are teaching a 15-year-old student who has never programmed before.
Explain what an API is in less than 150 words.
Use a restaurant waiter analogy.
Then give one simple software example.
Finish with one question to check the student's understanding.
```

Do they produce the same quality and structure of answer?

If not:

> **Why can changing only the words of our instruction change the quality, style, structure, and usefulness of an LLM response?**

That is where the next lesson begins:

# Prompt Engineering

---

## Security reminder

Never commit your real `.env` file or API keys to GitHub.

Before sharing this folder with students, keep only placeholder keys in `.env`.
