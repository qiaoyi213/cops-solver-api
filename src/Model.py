from pydantic import BaseModel
from typing import Set

class SubsetSumModel(BaseModel):
    S: Set[int]
    target: int