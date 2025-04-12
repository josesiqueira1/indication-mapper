from concurrent import futures
import grpc
from app.proto.drug_mapper_pb2 import (
    MapIndicationsRequest,
    MapIndicationsResponse,
    ICD10Mapping as ProtoICD10Mapping,
)
from app.proto.drug_mapper_pb2_grpc import (
    DrugMapperServicer,
    add_DrugMapperServicer_to_server,
)


class DrugMapperService(DrugMapperServicer):
    def MapIndications(
        self, request: MapIndicationsRequest, context
    ) -> MapIndicationsResponse:
        pass


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DrugMapperServicer_to_server(DrugMapperService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()