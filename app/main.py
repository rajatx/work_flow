from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from app.routes import public, dashboard


app = FastAPI()

@app.exception_handler(307)
async def auth_error_handler(request: Request, exc):
    return RedirectResponse(url="/login")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(public.router)
app.include_router(dashboard.router)