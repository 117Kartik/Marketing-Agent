from agents.ingestion_agent import ingest
from agents.creative_agent import creative_agent
from agents.personalization_agent import personalization_agent
from agents.optimizer_agent import optimizer_agent
from agents.approval_agent import approval_agent
from agents.publishing_agent import publishing_agent

from data_layer.database import init_db, save_campaign
from utils.rate_limiter import is_allowed


def run_pipeline():
    # 🔐 Initialize database (runs once safely)
    init_db()

    # 🔐 Rate limit check
    if not is_allowed():
        print("⚠️ Rate limit exceeded. Try again later.")
        return

    product = input("Enter product: ").strip()
    audience = input("Enter audience: ").strip()

    # 🔐 Input validation
    if not product or not audience:
        print("❌ Invalid input. Please try again.")
        return

    data = ingest(product, audience)

    while True:
        # 🤖 Multi-agent pipeline
        data = creative_agent(data)
        data = personalization_agent(data)
        data = optimizer_agent(data)

        decision = approval_agent(data).lower().strip()

        if decision == "publish":
            save_campaign(data)  # 🔥 auto-save on publish
            publishing_agent(data)
            print("Campaign published and saved!")
            break

        elif decision == "save":
            save_campaign(data)
            print("Campaign saved successfully!")
            break

        elif decision == "retry":
            print("\nRegenerating content...\n")
            continue

        elif decision == "cancel":
            print("Operation cancelled.")
            break

        else:
            print("⚠️ Invalid choice. Please type: publish / save / retry / cancel")


if __name__ == "__main__":
    run_pipeline()