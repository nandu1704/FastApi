from fastapi import FastAPI, File, UploadFile
import os
import uvicorn

app = FastAPI()

if not os.path.exists("resources"):
    os.makedirs("resources")
    
    
@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location= os.path.join("resources", file.filename)
    with open(file_location, "wb") as file_object:
        file_object.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, workers=1)