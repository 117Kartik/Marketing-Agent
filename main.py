from agents.ingestion_agent import ingest
from agents.creative_agent import creative_agent
from agents.personalization_agent import personalization_agent
from agents.optimizer_agent import optimizer_agent
from agents.approval_agent import approval_agent
from agents.publishing_agent import publishing_agent

def run_pipeline():
    product = input("Enter product: ")
    audience = input("Enter audience: ")

    data = ingest(product, audience)

    while True:
        data = creative_agent(data)
        data = personalization_agent(data)
        data = optimizer_agent(data)

        decision = approval_agent(data)

        if decision == "publish":
            publishing_agent(data)
            break
        elif decision == "retry":
            continue
        else:
            break

if __name__ == "__main__":
    run_pipeline()