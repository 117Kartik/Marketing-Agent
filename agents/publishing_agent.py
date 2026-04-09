from apis.linkedin_api import post_to_linkedin

def publishing_agent(data):
    post_to_linkedin(data['content'])