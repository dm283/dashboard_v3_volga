import os
from datetime import datetime
from fastapi import FastAPI, status, UploadFile, Form, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext
from app import models, schemas
from app.database import engine
from app.auth_section import get_db, Token, post_token, UserAuth, get_current_active_user, get_user_by_login, get_user
from app.service_functions import redefine_schema_values_to_none, load_excel

app = FastAPI()
origins = ["*",]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"], )

models.Base.metadata.create_all(bind=engine)   # creates db tables

# create token endpoint
@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
                                 db: Session=Depends(get_db)) -> Token:
    #
    return post_token(form_data, db)


# check fastapi is active endpoint
@app.get('/')
async def index():
    return {'message': 'fastapi server is working'}


#########################################################    SERVICE ENDPOINTS
# upload file excel
@app.put("/upload_file/")
async def upload_file(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                    entity: Annotated[str, Form()], file: UploadFile, db: Session = Depends(get_db)):
    try:
        filecontent = file.file.read()
        if not os.path.exists('uploaded_files'):
            os.makedirs("uploaded_files")
        file_location = f"uploaded_files/{file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(filecontent)
    except Exception as e:
        msg = {'status': 'error', 'message': 'file uploading or saving error', 'exception': str(e)}
        print(msg)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'ошибка загрузки или сохранения файла на сервере')

    load_res = load_excel(entity, file_location, db=db)

    return load_res


#########################################################    GET LIST OF ITEMS ENDPOINTS
@app.get("/goods_under_procedure/", response_model=list[schemas.GoodsUnderProcedure])
def read_records(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #
    return db.query(models.GoodsUnderProcedure).order_by(models.GoodsUnderProcedure.created_datetime.desc()).offset(skip).limit(limit).all()
    

@app.get("/goods_produced/", response_model=list[schemas.GoodsProduced])
def read_records(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #
    return db.query(models.GoodsProduced).order_by(models.GoodsProduced.created_datetime.desc()).offset(skip).limit(limit).all()


@app.get("/goods_usage/", response_model=list[schemas.GoodsUsage])
def read_records(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                  skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #
    return db.query(models.GoodsUsage).order_by(models.GoodsUsage.created_datetime.desc()).offset(skip).limit(limit).all()


#########################################################    CREATE ITEM ENDPOINTS
def create_item(data, db, model, schema):
    #
    data_none_values_redefined = redefine_schema_values_to_none(data, schema)
    db_item = model(**data_none_values_redefined.model_dump())
    try:
        db.add(db_item); db.commit(); db.refresh(db_item)
    except Exception as err:
        print(err)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return db_item


@app.post("/goods_under_procedure/", response_model=schemas.GoodsUnderProcedure)
def create_new_item(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   data: Annotated[schemas.GoodsUnderProcedureCreate, Form()], db: Session = Depends(get_db)):
    #
    return create_item(data=data, db=db, model=models.GoodsUnderProcedure, schema=schemas.GoodsUnderProcedureCreate)


@app.post("/goods_produced/", response_model=schemas.GoodsProduced)
def create_new_item(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   data: Annotated[schemas.GoodsProducedCreate, Form()], db: Session = Depends(get_db)):
    #
    return create_item(data=data, db=db, model=models.GoodsProduced, schema=schemas.GoodsProducedCreate)


@app.post("/goods_usage/", response_model=schemas.GoodsUsage)
def create_new_item(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   data: Annotated[schemas.GoodsUsageCreate, Form()], db: Session = Depends(get_db)):
    #
    return create_item(data=data, db=db, model=models.GoodsUsage, schema=schemas.GoodsUsageCreate)


#########################################################    DELETE ITEM ENDPOINTS
def delete_item(db: Session, item_id: int, model):
    #
    item_from_db =  db.query(model).filter(model.id==item_id).first()
    if item_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    try:
        db.delete(item_from_db)
        db.flush()
    except IntegrityError as err:
        db.rollback()
        table_name = err.args[0].partition('таблицы "')[2].partition('"\n')[0]
        msg_detail = f'Ошибка при удалении - есть связанные объекты в таблице {table_name}'
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg_detail)
    db.commit()

    return {"message": f"id {item_id} deleted successfully"}


@app.delete('/goods_under_procedure/{item_id}')
def delete_i(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   item_id: int, db: Session = Depends(get_db)):
    #
    return delete_item(db=db, item_id=item_id, model=models.GoodsUnderProcedure)


@app.delete('/goods_produced/{item_id}')
def delete_i(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   item_id: int, db: Session = Depends(get_db)):
    #
    return delete_item(db=db, item_id=item_id, model=models.GoodsProduced)


@app.delete('/goods_usage/{item_id}')
def delete_i(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   item_id: int, db: Session = Depends(get_db)):
    #
    return delete_item(db=db, item_id=item_id, model=models.GoodsUsage)


#########################################################    USERS ENDPOINTS
# def get_user_by_login(db: Session, login: str):
#     #
#     return db.query(models.User).filter(models.User.login==login).first()

@app.post("/users/", response_model=schemas.User)
def create_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                data: Annotated[schemas.UserCreate, Form()], db: Session = Depends(get_db)):
    #
    data_none_values_redefined = redefine_schema_values_to_none(data, schemas.UserCreate)
    if get_user_by_login(db, login=data_none_values_redefined.login):
        raise HTTPException(status_code=400, detail="Login already registered")
    password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    created_datetime = datetime.now()
    hashed_password=password_context.hash(data_none_values_redefined.password)
    db_user = models.User(
        **data_none_values_redefined.model_dump(exclude='password'),
        hashed_password=hashed_password, 
        created_datetime=created_datetime
        )
    db.add(db_user); db.commit(); db.refresh(db_user)
    return db_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(current_user: Annotated[UserAuth, Depends(get_current_active_user)], 
               skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    #
    return db.query(models.User).order_by(models.User.created_datetime.desc()).offset(skip).limit(limit).all()


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
              user_id: int, db: Session = Depends(get_db)):
    #
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/by_name/{username}", response_model=schemas.User)
def read_user_by_name(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
              username: str, db: Session = Depends(get_db)):
    #
    db_user = get_user(username=username, db=db)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put('/users/{item_id}', response_model=schemas.User)
def update_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                         item_id: int, data: Annotated[schemas.UserCreate, Form()], db: Session = Depends(get_db)):
    #
    updated_datetime = datetime.now()
    data_none_values_redefined = redefine_schema_values_to_none(data, schemas.UserCreate)
    item = schemas.UserUpdate(**data_none_values_redefined.model_dump(), updated_datetime=updated_datetime)

    item_from_db =  db.query(models.User).filter(models.User.id == item_id).first()
    if item_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    for field, value in item.model_dump(exclude_unset=True).items():
        setattr(item_from_db, field, value)
    db.commit()

    # password change
    new_pwd=data_none_values_redefined.password
    if new_pwd:
        password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        hashed_password=password_context.hash(new_pwd)
        setattr(item_from_db, 'hashed_password', hashed_password)
        db.commit()

    return item_from_db


@app.delete('/users/{item_id}')
def delete_user(current_user: Annotated[UserAuth, Depends(get_current_active_user)],
                   item_id: int, db: Session = Depends(get_db)):
    #
    item_from_db =  db.query(models.User).filter(models.User.id == item_id).first()
    if item_from_db is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    
    try:
        db.delete(item_from_db)
        db.flush()
    except IntegrityError as err:
        db.rollback()
        table_name = err.args[0].partition('таблицы "')[2].partition('"\n')[0]
        msg_detail = f'Ошибка при удалении - есть связанные объекты в таблице {table_name}'
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=msg_detail)
    db.commit()

    return {"message": f"User id {item_id} deleted successfully"}
