from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import auth, lessons, tasks, progress

app = FastAPI(
    title="Python Galaxy API",
    description="API прототипа образовательной платформы для изучения Python детьми 12+",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(lessons.router)
app.include_router(tasks.router)
app.include_router(progress.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
