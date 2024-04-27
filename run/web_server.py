import io
from os import walk
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse, StreamingResponse

from model import category_dict, try_on_cloth

app = FastAPI()


@app.get("/api/cloth/")
async def get_cloth_filenames():
    filenames = []
    for (dirpath, dirname, filename) in walk("./examples/garment/"):
        filenames.extend(filename)
        break
    return filenames


@app.get("/api/cloth/{filename}")
async def get_cloth_image(filename: str):
    image_path = Path(f"./examples/garment/{filename}")
    if not image_path.is_file():
        return {"error": "Cloth not found on the server"}
    return FileResponse(image_path)


@app.get("/api/model/")
async def get_model_filenames():
    filenames = []
    for (dirpath, dirname, filename) in walk("./examples/model/"):
        filenames.extend(filename)
        break
    return filenames


@app.get("/api/model/{filename}")
async def get_model_image(filename: str):
    image_path = Path(f"./examples/model/{filename}")
    if not image_path.is_file():
        return {"error": "Model not found on the server"}
    return FileResponse(image_path)


@app.get("/api/try_on/")
async def try_on_cloth_on_model(model_filename: str, cloth_filename: str, category: str):
    model_path = f"./examples/model/{model_filename}"
    cloth_path = f"./examples/garment/{cloth_filename}"
    if not Path(model_path).is_file():
        return {"error": "Model not found on the server"}
    if not Path(cloth_path).is_file():
        return {"error": "Cloth not found on the server"}
    if category not in category_dict:
        return {"error": "Wrong category, choose some from: " + str(category_dict)}
    image = try_on_cloth(model_path, cloth_path, category)
    imgio = io.BytesIO()
    image.save(imgio, 'JPEG')
    imgio.seek(0)
    return StreamingResponse(content=imgio, media_type="image/jpeg")
