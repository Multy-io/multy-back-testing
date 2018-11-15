import grpc
from services.eth_node_mock.proto import streamer_pb2, streamer_pb2_grpc


def run():
    with grpc.insecure_channel('127.0.0.1:6622') as channel:
        stub = streamer_pb2_grpc.NodeCommuunicationsStub(channel)
        new_block = stub.EventNewBlock(streamer_pb2.Empty())
        print('new block is', new_block)


if __name__ == '__main__':
    run()
