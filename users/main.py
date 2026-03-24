from fastapi import FastAPI
import uvicorn
import time

app = FastAPI()


@app.get("/hello")
def root():
    print("start")
    time.sleep(5)
    print("end")
    return "printed Successfully"


# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=8000, workers=1, limit_concurrency=2)
