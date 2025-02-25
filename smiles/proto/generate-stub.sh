python -m grpc_tools.protoc -I . --python_out=. ./computational_dp.proto
python -m grpc_tools.protoc -I . --python_out=. ./experimental_dp.proto
python -m grpc_tools.protoc -I . --python_out=. ./literature_dp.proto

# To generate the DataCatalog Stubs use the following command
#python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./data_catalog.proto
