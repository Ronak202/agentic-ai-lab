from tools import TOOLS

def select_tool(query):
    q = query.lower()
    if any(op in q for op in ['+', '-', '*', '/', 'calculate', 'compute']):
        return "calculator", query.replace("calculate","").replace("compute","").strip()
    elif "weather" in q:
        words = q.split()
        city = words[-1] if len(words) > 1 else "Mumbai"
        return "weather", city
    elif "summarize" in q or "summary" in q:
        text = query.split("summarize")[-1].strip()
        return "summarize", text
    return None, query

def run_agent():
    print("=== Tool-Using Agent (Assignment 2) ===")
    print("Tools: calculator, weather, summarize")
    print("Type 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() == "quit":
            break
        tool_name, arg = select_tool(query)
        if tool_name and tool_name in TOOLS:
            print(f"[Using tool: {tool_name}]")
            result = TOOLS[tool_name](arg)
        else:
            result = "No matching tool found. Try: 'calculate 5*5', 'weather London', 'summarize '"
        print(f"Agent: {result}\n")

if __name__ == "__main__":
    run_agent()
