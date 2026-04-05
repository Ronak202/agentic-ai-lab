import datetime

def get_input():
    return input("You: ").strip().lower()

def identify_intent(query):
    if any(op in query for op in ['+', '-', '*', '/']):
        return "calculate"
    elif "date" in query or "time" in query:
        return "datetime"
    elif any(word in query for word in ["hello", "hi", "hey"]):
        return "greet"
    elif "help" in query:
        return "help"
    else:
        return "unknown"

def execute_action(intent, query):
    if intent == "calculate":
        try:
            result = eval(query.replace("calculate", "").strip())
            return f"Result: {result}"
        except:
            return "Could not compute. Try: calculate 2 + 3"
    elif intent == "datetime":
        now = datetime.datetime.now()
        return f"Current date/time: {now.strftime('%Y-%m-%d %H:%M:%S')}"
    elif intent == "greet":
        return "Hello! I am your AI agent. How can I help you?"
    elif intent == "help":
        return "Commands: 'calculate X op Y', 'date', 'hello'"
    else:
        return "I don't understand that. Type 'help' for options."

def run_agent():
    print("=== Rule-Based AI Agent (Assignment 1) ===")
    print("Type 'quit' to exit.\n")
    while True:
        query = get_input()
        if query == "quit":
            print("Goodbye!")
            break
        intent = identify_intent(query)
        response = execute_action(intent, query)
        print(f"Agent: {response}\n")

if __name__ == "__main__":
    run_agent()
