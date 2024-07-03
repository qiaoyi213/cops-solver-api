from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Model import SubsetSumModel, MaximumCutModel
from Problem import SubsetSumProblem, MaximumCutProblem

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允許的前端域名
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)

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

@app.post("/cops/mcp")
def mcp_solve(problem: MaximumCutModel):
    print(problem.graph)
    mcp = MaximumCutProblem(list(problem.graph))

    answer = mcp.solve_SA()

    return answer

