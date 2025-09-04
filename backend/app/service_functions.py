import os
from datetime import datetime
from fastapi.exceptions import HTTPException
from fastapi import status
import pandas as pd


def redefine_schema_values_to_none(data, schema_obj):
    # get data received from frontend and redefine values if value is any kind of none to None
    data_dict = data.dict()
    for k in data_dict:
        if data_dict[k] in ['null', 'undefined', '']:
            data_dict[k] = None
    return schema_obj(**data_dict)


def upload_n_save_excel(file) -> str:
    #
    try:
        filecontent = file.file.read()
        if not os.path.exists('uploaded_files'):
            os.makedirs("uploaded_files")
        file_location = f"uploaded_files/{file.filename}"
        if os.path.exists(file_location):
            fname = file.filename.rpartition('.')[0] + datetime.now().strftime("_%d%m%Y%H%M%S") + '.' + file.filename.rpartition('.')[2]
            file_location = f"uploaded_files/{fname}"
        with open(file_location, "wb+") as file_object:
            file_object.write(filecontent)
    except Exception as e:
        msg = {'status': 'error', 'message': 'file uploading or saving error', 'exception': str(e)}
        print(msg)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'ошибка загрузки или сохранения файла на сервере')  
    return file_location


def transform_dataframe(df: pd.DataFrame, sections: list[str]) -> pd.DataFrame:
    #
    rows_with_section_name = list()
    sec = ''
    df['section'] = ''
    for index, row in df.iterrows():
        dict_row = row.to_dict()
        if dict_row['x1'] in sections:
            sec = dict_row['x1']
            rows_with_section_name.append(index)
            continue
        df.at[index, 'section'] = sec
    df.drop(rows_with_section_name, inplace=True)  # rows with section names deleting
    df.reset_index(inplace=True)
    return df


def excel_to_dataframe(file_location: str, sheet_name: str, header: int) -> pd.DataFrame:
    # read excel file and create pandas.DataFrame
    if not os.path.exists(file_location):
        return f"file {file_location} doesn't exits"
    try:
        df = pd.read_excel(io=file_location, sheet_name=sheet_name, header=header)
        df = df.add_prefix('x')
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'неверный формат файла')
    df = df.fillna('')
    # if len(df) == 0:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'0 записей в файле')
    return df
