#SRC_DIR="/Users/nvva/vhosts/multi-back-tests/multi-back-tests/services/eth_node_mock/proto"
#protoc -I=$SRC_DIR --python_out=$SRC_DIR $SRC_DIR/streamer.proto

python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. streamer.proto