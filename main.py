from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
from queue import Queue

testsQueue = FastAPI()
queue = Queue()


class BackendRequest(BaseModel):
    id: str
    code: str
    language: str
    tests: List[List[str]]
    stdio: bool
    input_file: str
    output_file: str


class BackendResponse(BaseModel):
    status: bool


class RunnerResponse(BackendResponse):
    any: bool
    id: str
    code: str
    language: str
    tests: List[List[str]]
    stdio: bool
    input_file: str
    output_file: str


@testsQueue.post("/solution", response_model=BackendResponse)
def queue_put(test: BackendRequest):
    queue.put(test)
    return JSONResponse({"status": True}, status_code=200)


@testsQueue.get("/solution", response_model=RunnerResponse)
def queue_get():
    if queue.empty():
        return JSONResponse({
            "any": False
        }, status_code=200)
    else:
        cur = queue.get()
        return JSONResponse({
            "any": True,
            "id": cur.id,
            "code": cur.code,
            "language": cur.language,
            "tests": cur.tests,
            "stdio": cur.stdio,
            "input_file": cur.input_file,
            "output_file": cur.output_file
        }, status_code=200)
