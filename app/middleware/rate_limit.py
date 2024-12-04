from fastapi import HTTPException, Request
import time

# 简单的用户速率限制
USER_REQUESTS = {}


def rate_limit(request: Request):
    user_id = request.headers.get("user-id")  # 假设用 user-id header 传递 user ID
    current_time = time.time()

    if user_id in USER_REQUESTS:
        requests = USER_REQUESTS[user_id]
        requests = [r for r in requests if current_time - r < 60 * 60]  # 1小时内的请求

        if len(requests) >= 100:  # 限制每个用户每小时最多100次请求
            raise HTTPException(status_code=429, detail="Too many requests")

        requests.append(current_time)
    else:
        USER_REQUESTS[user_id] = [current_time]