from app.api.rpc.pb2 import auth_pb2_grpc
from app.api.rpc.pb2 import auth_pb2
import grpc


def run():
    with grpc.insecure_channel("localhost:5001") as channel:
        stub = auth_pb2_grpc.AuthenticateStub(channel)
        request = auth_pb2.AuthenticateRequest(username="admin@gmail.com", password="admin@123")
        hello_reply = stub.authenticate(request)
        print(hello_reply)


if __name__ == "__main__":
    run()
