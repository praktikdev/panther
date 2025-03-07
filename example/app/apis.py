from datetime import timedelta

from panther.app import API
from panther.authentications import JWTAuthentication
from panther.logger import logger
from panther.request import Request
from panther.response import Response
from panther.db.connection import redis
from panther.throttling import Throttling

from app.serializers import UserInputSerializer, UserOutputSerializer
from app.models import User
from core.permissions import UserPermission


@API()
async def return_none():
    return None


@API(cache=True)
async def return_dict():
    return {'detail': 'ok'}


@API()
async def return_list():
    return [1, 2, 3]


@API()
async def return_tuple():
    return 1, 2, 3, 4


@API()
async def return_response_none():
    return Response()


@API()
async def return_response_dict():
    return Response(data={'detail': 'ok'}, status_code=201)


@API()
async def return_response_list():
    return Response(data=['car', 'home', 'phone'], status_code=202)


@API()
async def return_response_tuple():
    return Response(data=('car', 'home', 'phone', 'book'), status_code=202)


@API(input_model=UserInputSerializer)
async def res_request_data(request: Request):
    return Response(data=request.data)


@API(input_model=UserInputSerializer, output_model=UserOutputSerializer)
async def res_request_data_with_output_model(request: Request):
    return Response(data=request.data)


@API(input_model=UserInputSerializer)
async def using_redis(request: Request):
    redis.set('ali', '1')
    logger.debug(f"{redis.get('ali') = }")
    return Response()


@API()
async def login():
    user = User.insert_one(username='Ali', password='xxxx')
    token = JWTAuthentication.encode_jwt(user.id)
    return Response(token)


@API(auth=True)
async def auth_true(request: Request):
    return Response(request.user)


@API(auth=True, permissions=[UserPermission])
async def check_permission(request: Request):
    return Response(request.user)


@API(throttling=Throttling(rate=5, duration=timedelta(minutes=1)))
async def rate_limit():
    return Response(data=('car', 'home', 'phone', 'book'), status_code=202)


@API()
async def single_user(request: Request):
    # users = User.insert_one(username='Ali', password='1', age=12)
    users = User.find(id="64bd711cd73aa4a30786db77")
    print(f'{users=}')
    # # print(f'{dir(request) = }')
    # print(f'{request.data = }')
    # # print(f'{request.query_params = }')
    #
    # user = User.create_and_commit(username='ali', password='123')
    # # print(f'{user = }')
    # # print(f'{user.username = }')
    #
    # redis.set('ali', '1')
    # logger.debug(f"{redis.get('ali') = }")
    #
    # get_user = User.get_one(username='ali', password='123')
    # # print(f'{get_user = }')
    #
    # get_users = User.list()
    # # for u in get_users:
    # #     print(f'{u.id = }')
    # #     print(f'{u.username = }')
    #
    # last_user = User.last()
    # # print(f'{last_user.id = }')
    #
    # # raise UserNotFound
    # a = [
    #     {
    #         'id': 1,
    #         'username': 'ali',
    #         'password': '111',
    #     },
    #     {
    #         'id': 2,
    #         'username': 'ali2',
    #         'password': '1112',
    #     },
    #     {
    #         'id': 3,
    #         'username': 'ali3',
    #         'password': '1113',
    #     }
    # ]
    # b = 'asdf'
    # c = {1, 2, 4}
    #
    # class A:
    #     ...
    # d = A()
    # e = True
    # return Response(status_code=200, data=a)
    return Response(status_code=200)


# @API(input=UserInputSerializer, output_model=UserSerializer)
def create_user(request, body):
    return {'detail': 'ok'}

