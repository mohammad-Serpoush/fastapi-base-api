from concurrent import futures
import grpc
from api.rpc.auth import AuthServices
from api.rpc.pb2 import auth_pb2_grpc


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthenticateServicer_to_server(AuthServices(), server)

    server.add_insecure_port("0.0.0.0:5001")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    print("Running rpc server on localhost:5001")
    serve()
