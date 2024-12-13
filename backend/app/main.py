import sys, json
from datetime import datetime, timedelta, timezone
from typing import Annotated, Union
from pathlib import Path
from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import jwt
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel
from app.database import (select_dashboard_data, )


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

BASE_DIR = Path(__file__).resolve().parent.parent.parent
users_file = BASE_DIR / 'data/users/users_list.json'

try:
    #  при отсутствии файла с пользователями вход без страницы аутентификации
    with open(users_file, 'r') as jsonfile:
        USERS_LIST = json.load(jsonfile)  # type = dict
    # IS_AUTH_REQUIRED = True
    # IS_AUTHORIZED = False
    # print('THE FILE HAS FOUNDED, AUTH IS REQUIRED!', USERS_LIST)
except FileNotFoundError:
    # IS_AUTH_REQUIRED = False
    # IS_AUTHORIZED = True
    # print('THE FILE HAS NOT FOUNDED, AUTH IS NOT REQUIRED!')
    print('Users file is not founded! Exit script.')
    sys.exit()


fake_users_db = USERS_LIST

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app = FastAPI()

origins = [
    "*",
    # "http://localhost",
    # "http://127.0.0.1",
    # "http://localhost:8000",
    # "http://localhost:8080",
    # "http://localhost:5173",
    # "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def verify_password(plain_password, hashed_password):
    #
    return plain_password == hashed_password
    # return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.get('/')
async def index():
    return {'message': 'fastapi server is working'}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


######################
# @app.post('/dashboard/signin', status_code=status.HTTP_202_ACCEPTED)
# async def user_sign_in(
#     login: Union[str, None] = None,
#     password: Union[str, None] = None,
# ):
#     # user authentification
#     # global IS_AUTHORIZED
    
#     # print(f'!!!!!! post request = *{login}* *{password}*') ######

#     if not IS_AUTH_REQUIRED:
#         return {'message': 'authorization is not required'}
    
#     # if IS_AUTH_REQUIRED and IS_AUTHORIZED:
#     #     return {'message': 'authorization has already done'}

#     if (not login) or (not password):
#         raise HTTPException(
#             status_code=401,
#             detail='Incorrect username or password',
#         )
        
#     if login in USERS_LIST and USERS_LIST[login] == password:
#         # IS_AUTHORIZED = True

#         new_token = str(random.randint(1, 1000000))
#         TOKEN_LIST.append(new_token)
#         # print('new_token, TOKEN_LIST =', new_token, TOKEN_LIST) ##

#         # return {'user': login}
#         return {'your_new_token': new_token}
#     else:
#         raise HTTPException(
#             status_code=401,
#             detail='Incorrect username or password',
#         )
    

# @app.post('/dashboard/signout', status_code=status.HTTP_200_OK)
# async def user_sign_out(
#     token: Union[str, None] = None,
# ):
#     # user sign out
#     # global IS_AUTHORIZED

#     if IS_AUTH_REQUIRED:
#         # IS_AUTHORIZED = False
        
#         # print('token =', token)  ## 
#         TOKEN_LIST.remove(token)
#         # print('removed, updated TOKEN_LIST =', TOKEN_LIST)  ##
        
#         return {'message': 'signed out'}
#     else:
#         return {'message': 'there was not an authorization'}


@app.get('/dashboard/', status_code=status.HTTP_200_OK)
async def get_dashboard_data_filtered(
        current_user: Annotated[User, Depends(get_current_active_user)],
        # token: Union[str, None] = None,
        filterForeignGoodsDateFrom: Union[str, None] = None,
        filterForeignGoodsDateTo: Union[str, None] = None,
        filterEaesGoodsDateFrom: Union[str, None] = None,
        filterEaesGoodsDateTo: Union[str, None] = None,

        # filterArrivalDateFrom: Union[str, None] = None,
        # filterArrivalDateTo: Union[str, None] = None,
        # filterGoodsMovementDateOpFrom: Union[str, None] = None,
        # filterGoodsMovementDateOpTo: Union[str, None] = None,

        # filterAccountBookDateDocFrom: Union[str, None] = None,
        # filterAccountBookDateDocTo: Union[str, None] = None,
        # filterAccountBookDateEnterFrom: Union[str, None] = None,
        # filterAccountBookDateEnterTo: Union[str, None] = None,
        # filterReportVehicleDateEnterFrom: Union[str, None] = None,
        # filterReportVehicleDateExitTo: Union[str, None] = None,
        ):
    
    # if IS_AUTH_REQUIRED and (not token or token not in TOKEN_LIST):
    #     raise HTTPException(
    #         status_code=401,
    #         detail='Unauthorized',
    #     )
    
    # if IS_AUTH_REQUIRED and (not IS_AUTHORIZED):
    #     raise HTTPException(
    #         status_code=401,
    #         detail='Unauthorized',
    #     )
    
    # return {'message': 'ok! data is received'}

    try:
        filters = {
            "filterForeignGoodsDateFrom": filterForeignGoodsDateFrom,
            "filterForeignGoodsDateTo": filterForeignGoodsDateTo,
            "filterEaesGoodsDateFrom": filterEaesGoodsDateFrom,
            "filterEaesGoodsDateTo": filterEaesGoodsDateTo,
            # "filterAccountBookDateEnterFrom": filterAccountBookDateEnterFrom,
            # "filterAccountBookDateEnterTo": filterAccountBookDateEnterTo,
            # "filterReportVehicleDateEnterFrom": filterReportVehicleDateEnterFrom,
            # "filterReportVehicleDateExitTo": filterReportVehicleDateExitTo,
                }

        return select_dashboard_data(
            #selects_keys_list=['received_product_quantity', 'received_dt_quantity', 'received_tnved_quantity', 'account_book', 'report_vehicle'], 
            filters=filters)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'Error {e}'
        )
    #'received_product_quantity', 'received_dt_quantity', 'received_tnved_quantity', 
