def approval_agent(data):
    print("\n--- GENERATED CONTENT ---\n")
    print(data['content'])

    print("\n--- IMAGE ---\n")
    print("Saved at:", data.get("image_path"))

    print("\n-------------------------\n")

    choice = input("Approve? (publish / save / retry / cancel): ").lower().strip()
    return choice