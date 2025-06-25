from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from YDDownloader import YandexDiskDownloader
import uvicorn

app = FastAPI()
downloader = YandexDiskDownloader()

# Настройка статических файлов и шаблонов
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# API endpoints
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/download")
async def download_files(
        request: Request,
        seller: str = Form(...),
        call_type: str = Form(...),
        limit: int = Form(5),
        step: int = Form(1)
):
    result = downloader.download_files(seller, call_type, limit, step)
    return templates.TemplateResponse("results.html", {
        "request": request,
        "result": result
    })


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)