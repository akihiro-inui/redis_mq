from pydantic import BaseModel
from typing import List


class QueuedValue(BaseModel):
    array: List[int]
