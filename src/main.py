from typing import Union

from fastapi import FastAPI

from Model import SubsetSumModel
from Problem import SubsetSumProblem

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.post("/cops/ssp")
def ssp_solve(problem: SubsetSumModel):
    
    ssp = SubsetSumProblem(list(problem.S), int(problem.target))

    answer = ssp.solve_SA()
    
    return answer
