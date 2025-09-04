import os
from fastapi.exceptions import HTTPException
from fastapi import status
from app import schemas


def redefine_schema_values_to_none(data, schema_obj):
    # get data received from frontend and redefine values if value is any kind of none to None
    data_dict = data.dict()
    for k in data_dict:
        if data_dict[k] in ['null', 'undefined', '']:
            data_dict[k] = None
    return schema_obj(**data_dict)


# upload file excel (new 26.08.25)
def load_excel(entity, file_location, db):
    #
    import pandas as pd

    if not os.path.exists(file_location):
        return f"file {file_location} doesn't exits"
    
    try:
        df = pd.read_excel(file_location)
        print(df)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'неверный формат файла')

    df = df.fillna('')
    if len(df) == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'0 записей в файле')

    try:
        cnt = 0
        if entity == 'clients':
            for index, row in df.iterrows():
                dict_row = row.to_dict()
                dict_row.update(type='V')
                for i in dict_row:
                    dict_row[i] = str(dict_row[i])
                dict_row.update(inn=str(int(dict_row['inn'])))
                data = schemas.GoodsUnderProcedureCreate(**dict_row)
                data_none_values_redefined = redefine_schema_values_to_none(data, schemas.GoodsUnderProcedureCreate)
                # print('data_none_values_redefined =', data_none_values_redefined)
                # prevalidation = schemas.ContactValidation(**data_none_values_redefined.model_dump())
                # print('prevalidation =', prevalidation)
                # res = crud.create_contact(db=db, item=data_none_values_redefined)
                cnt += 1
    except Exception as e:
        msg = {'status': 'error', 'message': f'создано {cnt} объектов, на строке {cnt+1} ошибка контента', 'exception': str(e)}
        print(msg)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'создано объектов - {cnt}, на строке {cnt+1} ошибка контента')

    
    return {'status_code': status.HTTP_201_CREATED, 'detail': f'ok. создано объектов - {cnt}'}
