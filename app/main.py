from fastapi import FastAPI
from app.routers  import tenencia


app = FastAPI() 

app.include_router(tenencia.router)



@app.get("/")
async def index():
    return {"message": "index"}





