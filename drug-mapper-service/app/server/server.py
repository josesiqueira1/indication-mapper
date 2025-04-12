from concurrent import futures

import grpc
from app.grpc.service import DrugMapperService
from app.proto.drug_mapper_pb2_grpc import add_DrugMapperServicer_to_server


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    add_DrugMapperServicer_to_server(DrugMapperService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()
