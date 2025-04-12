import pytest
from app.llm.mapper import map_indications_to_icd10
from app.models.indication import DrugIndication


def test_map_indications_to_icd10(monkeypatch):
    dummy_response = {
        "drug_name": "Dupixent",
        "set_id": "1234-setid",
        "indications": [
            "moderate-to-severe atopic dermatitis",
            "chronic rhinosinusitis with nasal polyps",
        ],
        "icd10_mappings": [
            {"code": "L20.84", "description": "Intrinsic (allergic) eczema"},
            {"code": "J33.1", "description": "Nasal polyp"},
        ],
    }

    class MockOpenAI:
        @staticmethod
        def ChatCompletion_create(*args, **kwargs):
            class Response:
                def __getitem__(self, key):
                    return {"choices": [{"message": {"content": str(dummy_response)}}]}[
                        key
                    ]

            return Response()

    monkeypatch.setattr(
        "app.llm.mapper.openai.ChatCompletion.create", MockOpenAI.ChatCompletion_create
    )

    result = map_indications_to_icd10(
        drug_name="Dupixent",
        set_id="1234-setid",
        text="Some long drug indication text...",
    )

    assert isinstance(result, DrugIndication)
    assert result.drug_name == "Dupixent"
    assert len(result.indications) == 2
    assert result.icd10_mappings[0].code == "L20.84"
