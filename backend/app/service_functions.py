import os
from fastapi.exceptions import HTTPException
from fastapi import status
import pandas as pd
from app import schemas


def redefine_schema_values_to_none(data, schema_obj):
    # get data received from frontend and redefine values if value is any kind of none to None
    data_dict = data.dict()
    for k in data_dict:
        if data_dict[k] in ['null', 'undefined', '']:
            data_dict[k] = None
    return schema_obj(**data_dict)


def upload_n_save_excel(file):
    #
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
    return file_location


def read_excel(file_location: str) -> pd.DataFrame:
    # read excel file 
    if not os.path.exists(file_location):
        return f"file {file_location} doesn't exits"
    
    try:
        df = pd.read_excel(io=file_location, sheet_name='использование_товаров', header=3)
        df = df.add_prefix('x')
        print(df)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'неверный формат файла')

    df = df.fillna('')
    if len(df) == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'0 записей в файле')

    return df
