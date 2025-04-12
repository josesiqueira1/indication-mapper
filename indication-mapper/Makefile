.PHONY: generate-grpc

generate-grpc:
	python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. app/proto/drug_mapper.proto