# TODO:
# 1. Take uploaded images and run them through the ML vision thing?
# 2. take the outputed location and pull a descirption
# 3. figure out how to get the description, web scraping, or google api, or manual?

from fastapi import FastAPI, UploadFile

app = FastAPI()

data = {'Suzzallo': "Suzzallo is a library"}

@app.get("/description/{location}")
async def read_item(location: str):
    return {"description": data[location]}


@app.post("/upload/")
async def create_upload_file(file: UploadFile):
    return {"description": data['Suzzallo'], "filename": file.filename}