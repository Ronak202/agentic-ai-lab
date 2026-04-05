import os, json, datetime
from tools import TOOLS
from dotenv import load_dotenv
load_dotenv()

try:
    from groq import Groq
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    USE_LLM = True
    print("Groq connected OK")
except Exception as e:
    print(f"Groq failed: {e} — using simulation")
    USE_LLM = False

LOG_FILE = "day3/agent_log.txt"

def log(entry):
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

def llm_select_tool(query):
    if not USE_LLM:
        return simulate_tool_selection(query)
    system = (
        "You are a tool-selection assistant. "
        "Reply ONLY with JSON: {\"tool\": \"\", \"arg\": \"\"}\n"
        "Available tools:\n"
        "  calculator — for any math or arithmetic\n"
        "  weather    — for weather or temperature of a city\n"
        "  summarize  — for summarizing any text\n"
        "If no tool fits: {\"tool\": \"none\", \"arg\": \"\"}\n"
        "Do not add explanation. JSON only."
    )
    resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "system", "content": system},
                  {"role": "user",   "content": query}]
    )
    raw = resp.choices[0].message.content.strip()
    try:
        return json.loads(raw)
    except:
        return simulate_tool_selection(query)

def simulate_tool_selection(query):
    q = query.lower()
    if any(op in q for op in ['+','-','*','/','calculate','compute','sum','add']):
        return {"tool": "calculator", "arg": q.replace("calculate","").strip()}
    elif any(w in q for w in ["weather","temperature","temp","climate"]):
        words = q.split()
        city = words[-1] if words else "Mumbai"
        return {"tool": "weather", "arg": city}
    elif "summarize" in q or "summary" in q or len(q.split()) > 6:
        text = query.split("summarize")[-1].strip().strip('"')
        return {"tool": "summarize", "arg": text}
    return {"tool": "none", "arg": ""}

def run_agent():
    mode = "REAL LLM (Groq)" if USE_LLM else "SIMULATED"
    print(f"\n=== LLM-Based Agent (Assignment 3) — {mode} ===")
    print("Type 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() == "quit":
            print("Goodbye!")
            break
        decision  = llm_select_tool(query)
        tool_name = decision.get("tool", "none")
        arg       = decision.get("arg", query)
        if tool_name in TOOLS:
            print(f"[Tool selected: {tool_name} | Arg: {arg}]")
            result = TOOLS[tool_name](arg)
        else:
            result = "No suitable tool found for this query."
        print(f"Agent: {result}\n")
        log({"time": str(datetime.datetime.now()),
             "input": query, "tool": tool_name, "output": result})

if __name__ == "__main__":
    run_agent()
