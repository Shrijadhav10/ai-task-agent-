from agent import run_agent

while True:
    query = input("\nYou: ")
    print("\nAgent:", run_agent(query))
