from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


gol_frontend_templates = Jinja2Templates(directory="../../gol-frontend")

@app.get("/page", response_class=HTMLResponse)
async def read_page(request: Request):
    return gol_frontend_templates.TemplateResponse("admin_page/index.html", {"request": request})