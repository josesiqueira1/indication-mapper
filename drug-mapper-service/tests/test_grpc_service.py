import pytest
from app.grpc.service import DrugMapperService
from app.models.indication import DrugIndication
from app.proto.drug_mapper_pb2 import MapIndicationsRequest
from tests.test_helper import VALID_SETID
import grpc


@pytest.fixture
def service():
    return DrugMapperService()


@pytest.fixture
def sample_mapping():
    return DrugIndication(
        set_id=VALID_SETID,
        indications=[
            "moderate-to-severe atopic dermatitis",
            "chronic rhinosinusitis with nasal polyps",
        ],
        icd10_mappings=[
            {"code": "L20.84", "description": "Intrinsic (allergic) eczema"},
            {"code": "J33.1", "description": "Nasal polyp"},
        ],
    )


class MockContext:
    def __init__(self):
        self.code = None
        self.details = None

    def set_code(self, code):
        self.code = code

    def set_details(self, details):
        self.details = details


def test_map_indications_from_cache(monkeypatch, service, sample_mapping):
    # Mock cache to return cached data
    monkeypatch.setattr("app.grpc.service.get_cached_mapping", lambda _: sample_mapping)
    monkeypatch.setattr("app.grpc.service.cache_mapping", lambda _, __: None)

    request = MapIndicationsRequest(
        set_id=VALID_SETID,
    )
    context = MockContext()

    response = service.MapIndications(request, context)

    assert response.set_id == VALID_SETID
    assert len(response.indications) == 2
    assert len(response.icd10_mappings) == 2
    assert response.icd10_mappings[0].code == "L20.84"


def test_map_indications_from_llm(monkeypatch, service, sample_mapping):
    # Mock cache to return None (cache miss)
    monkeypatch.setattr("app.grpc.service.get_cached_mapping", lambda _: None)
    monkeypatch.setattr("app.grpc.service.cache_mapping", lambda _, __: None)
    # Mock mapper to return sample mapping
    monkeypatch.setattr(
        "app.grpc.service.map_indications_to_icd10",
        lambda *args, **kwargs: sample_mapping,
    )

    request = MapIndicationsRequest(
        set_id=VALID_SETID,
    )
    context = MockContext()

    response = service.MapIndications(request, context)

    assert response.set_id == VALID_SETID
    assert len(response.indications) == 2
    assert len(response.icd10_mappings) == 2
    assert response.icd10_mappings[0].code == "L20.84"


def test_map_indications_error(monkeypatch, service):
    # Mock cache to return None (cache miss)
    monkeypatch.setattr("app.grpc.service.get_cached_mapping", lambda _: None)
    # Mock mapper to raise an error
    monkeypatch.setattr(
        "app.grpc.service.map_indications_to_icd10",
        lambda *args, **kwargs: (_ for _ in ()).throw(Exception("Test error")),
    )

    request = MapIndicationsRequest(
        set_id=VALID_SETID,
    )
    context = MockContext()

    response = service.MapIndications(request, context)

    assert response.set_id == ""
    assert len(response.indications) == 0
    assert len(response.icd10_mappings) == 0
    assert context.code == grpc.StatusCode.INTERNAL
    assert context.details == "Test error"
