from datetime import timedelta

from app.api.rpc.pb2 import auth_pb2_grpc, auth_pb2
from app import services
from app.core import security
from app.core.config import settings
from app.core.unit_of_work import UnitOfWork
from app.db.session import SessionLocal


class AuthServices(auth_pb2_grpc.AuthenticateServicer):
    def authenticate(self, request, context):
        print("here")
        db = SessionLocal()
        with UnitOfWork(db) as uow:
            user = services.user.authenticate(
                uow,
                email=request.username,
                password=request.password
            )
            access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            token_payload = {
                "id": str(user.id),
            }

            token = security.create_access_token(
                token_payload, expires_delta=access_token_expires
            )
            res = auth_pb2.AuthenticateResponse()
            res.token = token
            res.type = "bearer"
            return res
