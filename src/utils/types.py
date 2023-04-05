from pydantic import BaseModel
from typing import List


class RegisterJobRequest(BaseModel):
    array: List[int]
