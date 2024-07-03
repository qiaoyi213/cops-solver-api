from pydantic import BaseModel
from typing import Set, List, Tuple

class SubsetSumModel(BaseModel):
    S: Set[int]
    target: int

class MaximumCutModel(BaseModel):
    graph: List[Tuple]
