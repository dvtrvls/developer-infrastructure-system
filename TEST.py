from fastapi import FastAPI

app= FastAPI()


@app.get("/")
async def root():
    return "<h1>root page</h1>"