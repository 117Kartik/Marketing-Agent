def approval_agent(data):
    content = data["content"]

    print("\n================ CAMPAIGN =================\n")

    print("Headline:")
    print(content.get("headline"))

    print("\nCaption:")
    print(content.get("caption"))

    print("\nHashtags:")
    for tag in content.get("hashtags", []):
        print("-", tag)

    print("\nCTA:")
    print(content.get("cta"))

    print("\nImage Path:")
    print(data.get("image_path"))

    print("\n==========================================\n")

    choice = input("Approve? (publish / save / retry / cancel): ").lower().strip()
    return choice