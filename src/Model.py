from pydantic import BaseModel
from typing import Set, List, Tuple

class SubsetSumModel(BaseModel):
    S: Set[int]
    target: int

class MaximumCutModel(BaseModel):
    graph: List[Tuple]

class VertexCoverModel(BaseModel):
    graph: List[Tuple]

class KnapsackModel(BaseModel):
    values: List[int]
    weights: List[int]
    capacity: int

class GraphColoringModel(BaseModel):
    graph: List[Tuple]
    num_colors: int

class HamiltonianCycleModel(BaseModel):
    graph: List[Tuple]

class TravellingSalespersonModel(BaseModel):
    graph: List[Tuple]

class JobShopSchedulingModel(BaseModel):
    jobs: List[Tuple]
    machines: List[Tuple] 


