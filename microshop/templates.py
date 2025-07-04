from fastapi.templating import Jinja2Templates
import pathlib

BASE_DIR = pathlib.Path(__file__).parent  # папка microshop
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))