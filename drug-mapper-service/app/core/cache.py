from app.models.indication import DrugIndication


def get_cached_mapping(setid: str) -> DrugIndication | None:
    return None


def cache_mapping(setid: str, mapping: DrugIndication):
    pass
