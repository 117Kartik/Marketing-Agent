def approval_agent(data):
    print("\n--- GENERATED CONTENT ---\n")
    print(data['content'])
    print("\n-------------------------\n")

    choice = input("Approve? (publish / retry / cancel): ")
    return choice