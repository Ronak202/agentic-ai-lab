import re

# ── Tools ──────────────────────────────────────────────
def extract_numbers(text):
    nums = re.findall(r'\d+\.?\d*', text)
    return [float(n) for n in nums]

def compute_average(numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

def generate_summary(numbers, avg):
    return (f"You provided {len(numbers)} numbers: {numbers}. "
            f"Their average is {avg:.2f}.")

# ── Planner ────────────────────────────────────────────
def plan_steps(query):
    """Break the query into ordered steps."""
    steps = []
    q = query.lower()
    if "average" in q or "mean" in q:
        steps.append(("extract",  "Extract numbers from query"))
        steps.append(("average",  "Compute the average"))
        steps.append(("summarize","Generate a natural language summary"))
    elif "calculate" in q or "compute" in q:
        steps.append(("extract",  "Extract numbers from query"))
        steps.append(("evaluate", "Evaluate math expression"))
    else:
        steps.append(("default",  "Handle as general query"))
    return steps

# ── Executor ───────────────────────────────────────────
def execute_steps(steps, query):
    print("\n--- Plan ---")
    for i, (_, desc) in enumerate(steps, 1):
        print(f"  Step {i}: {desc}")
    print("\n--- Execution ---")

    context = {}
    for action, desc in steps:
        print(f"\n[{action.upper()}] {desc}")
        if action == "extract":
            context["numbers"] = extract_numbers(query)
            print(f"  -> Numbers found: {context['numbers']}")
        elif action == "average":
            context["avg"] = compute_average(context.get("numbers", []))
            print(f"  -> Average: {context['avg']:.2f}")
        elif action == "summarize":
            context["summary"] = generate_summary(
                context.get("numbers", []),
                context.get("avg", 0))
            print(f"  -> Summary: {context['summary']}")
        elif action == "evaluate":
            try:
                expr = re.sub(r'[a-zA-Z]', '', query).strip()
                context["result"] = eval(expr)
                print(f"  -> Result: {context['result']}")
            except:
                context["result"] = "Could not evaluate"
                print(f"  -> {context['result']}")
        elif action == "default":
            context["result"] = "No specific action. Echoing: " + query
            print(f"  -> {context['result']}")

    print("\n--- Final Output ---")
    if "summary" in context:
        return context["summary"]
    if "result" in context:
        return str(context["result"])
    return "Task complete."

# ── Main ───────────────────────────────────────────────
def run_agent():
    print("=== Multi-Step Planning Agent (Assignment 4) ===")
    print("Example: 'Find the average of 5, 10, 15 and summarize'")
    print("Type 'quit' to exit.\n")
    while True:
        query = input("You: ").strip()
        if query.lower() == "quit":
            break
        steps  = plan_steps(query)
        result = execute_steps(steps, query)
        print(f"\nAgent: {result}\n")

if __name__ == "__main__":
    run_agent()
