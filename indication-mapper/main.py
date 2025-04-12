import app.dailymed.fetcher
from app.grpc.service import DrugMapperService
from app.proto.drug_mapper_pb2 import MapIndicationsRequest
import app.llm.mapper
from dotenv import load_dotenv

load_dotenv()

DRUG_ID = "595f437d-2729-40bb-9c62-c8ece1f82780"


def get_from_llm():
    indications = app.dailymed.fetcher.fetch_indications_section(DRUG_ID)

    maps = app.llm.mapper.map_indications_to_icd10(DRUG_ID, indications)

    print("Mapping Results:")
    for icd10_code, description in maps.icd10_mappings:
        print(f"{icd10_code[1]}: {description[1]}")


def get_from_service():
    class Context:
        def __init__(self):
            self.code = None
            self.details = None

        def set_code(self, code):
            self.code = code

        def set_details(self, details):
            self.details = details

    service = DrugMapperService()

    request = MapIndicationsRequest(
        set_id=DRUG_ID,
    )
    context = Context()

    response = service.MapIndications(request, context)
    print(response)
    print(context)


if __name__ == "__main__":
    # get_from_llm()
    get_from_service()
