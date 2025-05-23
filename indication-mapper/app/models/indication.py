from pydantic import BaseModel
from typing import List


class ICD10Mapping(BaseModel):
    code: str
    description: str


class DrugIndication(BaseModel):
    set_id: str
    indications: List[str]
    icd10_mappings: List[ICD10Mapping]
