from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import users
from database import engine, Base
from models import user

app = FastAPI(title="Vue3 + Python API", version="1.0.0")

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建数据库表
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# 注册路由
app.include_router(users.router, prefix="/api", tags=["users"])

@app.get("/")
async def root():
    return {"message": "Vue3 + Python API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)