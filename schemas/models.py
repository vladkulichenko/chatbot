from pydantic import BaseModel, Field
from typing import Dict, Optional, List


class Question(BaseModel):
    messages: Optional[List[Dict]] = Field(
        default=None,
        description="Historical messages",
        error_message={"Messages must be a list."},
        examples=[],
    )
    debug: Optional[bool] = Field(
        default=False,
        description="Debug mode",
        error_message={"Debug mode must be a boolean."},
        examples=[True],
    )
