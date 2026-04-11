import time

user_requests = {}

MAX_REQUESTS = 5      
TIME_WINDOW = 60        

def is_allowed(user="default"):
    current_time = time.time()

    if user not in user_requests:
        user_requests[user] = []

    # remove old requests
    user_requests[user] = [
        t for t in user_requests[user]
        if current_time - t < TIME_WINDOW
    ]

    if len(user_requests[user]) >= MAX_REQUESTS:
        return False

    user_requests[user].append(current_time)
    return True