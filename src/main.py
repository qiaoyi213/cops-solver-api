from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Model import *
from Problem import *

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
    mcp = MaximumCutProblem(list(problem.graph))

    answer = mcp.solve_SA()

    return answer
@app.post("/cops/vcp")
def vcp_solve(problem: VertexCoverModel):
    
    vcp = VertexCoverProblem(list(problem.graph))

    answer = vcp.solve_SA()

    return answer

@app.post("/cops/01kp")
def kp_solve(problem: KnapsackModel):
    kp = KnapsackProblem(list(problem.weights), list(problem.values),int(problem.capacity))

    answer = kp.solve_SA()

    return answer

@app.post("/cops/gcp")
def gcp_solve(problem: GraphColoringModel):
    gcp = GraphColoringProblem(list(problem.graph), int(problem.num_colors))

    answer = gcp.solve_SA()
    
    return answer

@app.post("/cops/hcp")
def hcp_solve(problem: HamiltonianCycleModel):
    hcp = HamiltonianCycleProblem(list(problem.graph))

    answer = hcp.solve_SA()

    return answer

@app.post("/cops/tsp")
def tsp_solve(problem: TravellingSalespersonModel):
    tsp = TravellingSalespersonProblem(list(problem.graph))

    answer = tsp.solve_SA()

    return answer