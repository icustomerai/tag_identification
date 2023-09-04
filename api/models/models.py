from pydantic import BaseModel
from typing import Optional,List,Dict

class input_tag_identification(BaseModel):
    websites : list[str]

class output_tag_identification(BaseModel):
    output : Dict   
