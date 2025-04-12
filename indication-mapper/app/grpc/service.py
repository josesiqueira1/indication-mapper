import grpc
from app.core.cache import get_cached_mapping, cache_mapping
from app.llm.mapper import map_indications_to_icd10
from app.models.indication import DrugIndication
from app.dailymed.fetcher import fetch_indications_section
from app.proto.drug_mapper_pb2 import (
    MapIndicationsRequest,
    MapIndicationsResponse,
    ICD10Mapping as ProtoICD10Mapping,
)
from app.proto.drug_mapper_pb2_grpc import DrugMapperServicer


class DrugMapperService(DrugMapperServicer):
    def MapIndications(
        self, request: MapIndicationsRequest, context
    ) -> MapIndicationsResponse:
        try:
            # Check cache first
            cached_mapping = get_cached_mapping(request.set_id)
            if cached_mapping:
                return self._convert_to_response(cached_mapping)

            # Fetch indications using fetcher
            indication_text = fetch_indications_section(request.set_id)
            if not indication_text:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(
                    f"Indications not found for set_id: {request.set_id}"
                )
                return MapIndicationsResponse()

            # Map indications to ICD-10 codes
            mapping = map_indications_to_icd10(
                set_id=request.set_id,
                text=indication_text,
            )

            # Cache the result
            cache_mapping(request.set_id, mapping)

            return self._convert_to_response(mapping)

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return MapIndicationsResponse()

    def _convert_to_response(self, mapping: DrugIndication) -> MapIndicationsResponse:
        return MapIndicationsResponse(
            set_id=mapping.set_id,
            indications=mapping.indications,
            icd10_mappings=[
                ProtoICD10Mapping(code=m.code, description=m.description)
                for m in mapping.icd10_mappings
            ],
        )
