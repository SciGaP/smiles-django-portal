python -m grpc_tools.protoc -I . --python_out=. ./computational_dp.proto
python -m grpc_tools.protoc -I . --python_out=. ./experimental_dp.proto
python -m grpc_tools.protoc -I . --python_out=. ./literature_dp.proto

# To generate the DataCatalog Stubs use the following command
#python -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. ./data_catalog.proto
# Generate the DataCatalog Stubs
python -m grpc_tools.protoc -I "D:/airavata-data-catalog/data-catalog-api/stubs/src/main/proto" --python_out="D:/smiles-django-portal/smiles/proto" --grpc_python_out="D:/smiles-django-portal/smiles/proto" "D:/airavata-data-catalog/data-catalog-api/stubs/src/main/proto/data_catalog.proto"