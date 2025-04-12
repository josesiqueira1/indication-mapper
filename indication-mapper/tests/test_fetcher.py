import pytest
from app.dailymed.fetcher import fetch_indications_section
from tests.test_helper import VALID_SETID, INVALID_SETID


def test_fetch_indications_success():
    text = fetch_indications_section(VALID_SETID)
    assert isinstance(text, str)
    assert "indicated" in text.lower() or "treatment" in text.lower()
    assert len(text) > 30


def test_fetch_indications_section_missing(monkeypatch):
    def mock_response(*args, **kwargs):
        class MockResp:
            status_code = 200

            def raise_for_status(self):
                pass

            @property
            def text(self):
                return "<document></document>"  # missing section

        return MockResp()

    monkeypatch.setattr("requests.get", mock_response)

    with pytest.raises(ValueError):
        fetch_indications_section("some-id")


def test_fetch_indications_invalid_setid():
    with pytest.raises(ValueError):
        fetch_indications_section(INVALID_SETID)
