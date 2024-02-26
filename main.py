from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pathlib import Path
from pebblo.app.service.local_ui_service import AppData
from fastapi.responses import FileResponse
from pebblo.app.enums.enums import CacheDir
from pebblo.app.utils.utils import get_full_path

app = FastAPI()

app.mount(
    "/pebblo/pebblo/app/pebblo-ui",
    StaticFiles(directory=Path(__file__).parent.parent.absolute()/"pebblo/pebblo/app/pebblo-ui"),
    name="static",
)

templates = Jinja2Templates(directory="pebblo/app/pebblo-ui")

@app.get("/pebblo/")
async def hello(request: Request):
      app_data = AppData()
      response = templates.TemplateResponse(request=request, name="index.html", context={"data": app_data.get_all_apps_details()})
      return response


@app.get("/pebblo/appDetails/")
async def hello(request: Request, app_name:str):
      app_data = AppData()
      response = templates.TemplateResponse("index.html", {"request": request, "data": app_data.get_app_details(app_name)})
      return response


@app.get("/pebblo/getReport/")
async def hello(request: Request, app_name:str):
      # File path for app report
      file_path = f'{get_full_path(CacheDir.home_dir.value)}/{app_name}/pebblo_report.pdf'
      # To view the file in the browser, use "inline" for the media_type
      headers = {
         'Access-Control-Expose-Headers': 'Content-Disposition'
      }
      # Create a FileResponse object with the file path, media type and headers
      response = FileResponse(file_path, filename="report.pdf", media_type="application/pdf", headers=headers)
      # Return the FileResponse object
      return response