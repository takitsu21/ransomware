from typing import Union

from fastapi import FastAPI


app = FastAPI(debug=True)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# Run app
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=12001)