from fastapi import FastAPI
from mangum import Mangum
from app.mootcourt.routers import router as token_router
from app.cases.routers import router as cases_router

app = FastAPI()
handler = Mangum(app)


app.include_router(token_router)
app.include_router(cases_router)

@app.get("/")
def root():
    return {"response": "testing deployment"}
