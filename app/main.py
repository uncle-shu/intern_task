from fastapi import FastAPI
from app.middleware.logging import log_requests
from app.middleware.rate_limit import rate_limit
from app.views import auth, tasks

app = FastAPI()

app.include_router(auth.router)
app.include_router(tasks.router)

app.middleware('http')(log_requests)
app.middleware('http')(rate_limit)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
