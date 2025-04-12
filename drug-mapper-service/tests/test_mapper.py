import pytest
from app.llm.mapper import map_indications_to_icd10
from app.models.indication import DrugIndication
import json


@pytest.fixture
def sample_response():
    return {
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
    def __init__(self):
        self.responses = MockResponses()


class MockResponses:
    def create(self, **kwargs):
        return self

    def __getattr__(self, name):
        if name == "output_text":
            return json.dumps(sample_response())
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


@pytest.fixture
def mock_openai(monkeypatch):
    mock = MockOpenAI()
    monkeypatch.setattr("app.llm.mapper.get_openai_client", lambda: mock)
    return mock


def test_map_indications_to_icd10(monkeypatch, sample_response, mock_openai):
    result = map_indications_to_icd10(
        drug_name="Dupixent", set_id="1234-setid", text="Sample indication text"
    )

    assert isinstance(result, DrugIndication)
    assert result.drug_name == "Dupixent"
    assert len(result.indications) == 2
    assert result.icd10_mappings[0].code == "L20.84"


class MockOpenAIInvalidResponse:
    def __init__(self, response_data):
        self.responses = MockResponsesInvalid(response_data)


class MockResponsesInvalid:
    def __init__(self, response_data):
        self.response_data = response_data

    def create(self, **kwargs):
        return self

    def __getattr__(self, name):
        if name == "output_text":
            return json.dumps(self.response_data)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )


@pytest.mark.parametrize(
    "invalid_response",
    [
        {"drug_name": "Missing fields"},
        {
            "drug_name": "Dupixent",
            "set_id": "1234",
            "indications": [],
        },  # Missing mappings
    ],
)
def test_map_indications_invalid_response(monkeypatch, invalid_response):
    mock = MockOpenAIInvalidResponse(invalid_response)
    monkeypatch.setattr("app.llm.mapper.get_openai_client", lambda: mock)

    with pytest.raises(ValueError):
        map_indications_to_icd10(
            drug_name="Dupixent", set_id="1234-setid", text="Sample indication text"
        )


class MockOpenAIError:
    def __init__(self):
        self.responses = MockResponsesError()


class MockResponsesError:
    def create(self, **kwargs):
        raise Exception("OpenAI API error")


def test_map_indications_openai_error(monkeypatch):
    mock = MockOpenAIError()
    monkeypatch.setattr("app.llm.mapper.get_openai_client", lambda: mock)

    with pytest.raises(Exception) as exc_info:
        map_indications_to_icd10(
            drug_name="Dupixent", set_id="1234-setid", text="Sample indication text"
        )

    assert "Error mapping indications" in str(exc_info.value)
