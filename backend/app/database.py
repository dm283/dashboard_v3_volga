import sys, os, configparser, pyodbc
from pathlib import Path
from abc import ABC, abstractmethod
from typing import Union
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent

config = configparser.ConfigParser()
config_file = BASE_DIR / 'config.ini'
if os.path.exists(config_file):
    config.read(config_file, encoding='utf-8')
else:
    print("error! config file doesn't exist"); sys.exit()


DB_CONNECTION_STRING = config['db']['db_connection_string']
DB_NAME = config['db']['db_name']
DB_SCHEMA = config['db']['db_schema']
COMPANY_NAME = config['content']['company_name']


class Database(ABC):
    """
    Database context manager
    """

    def __init__(self, driver) -> None:
        self.driver = driver

    @abstractmethod
    def connect_to_database(self):
        raise NotImplementedError()
    
    def __enter__(self):
        self.connection = self.connect_to_database()
        self.cursor = self.connection.cursor()
        return self
    
    def __exit__(self, exception_type, exc_val, traceback):
        self.cursor.close()
        self.connection.close()


class DBConnect(Database):
    """PyODBC Database context manager"""

    def __init__(self) -> None:
        self.driver = pyodbc
        super().__init__(self.driver)

    def connect_to_database(self):
        return self.driver.connect(DB_CONNECTION_STRING)


# ========================== ***  SELECTS SET  *** ============================ #
select = {}
filter_string_mark = '!filter_string_mark!'


# 1.Title=Иностранные товары
# 1.1  Иностранные товарары
select['foreign_goods_list'] = f"""
  SELECT guid_cat,goods,g33,ngtd+'/'+CAST(g32 AS VARCHAR) ngtd,namebux+' '+nbux+' '+CONVERT(VARCHAR,datebux,105) nbux,datebux,
    place,naccount,packs,ed_izm,packs_dt,g41a,
    packs_0,packs_1,packs_2,packs_3,packs_4,packs_5,packs_6,packs_7,packs_8
    FROM {DB_NAME}.{DB_SCHEMA}.REG_JR
    WHERE 1=1 {filter_string_mark}
    ORDER BY ngtd,datebux,guid_cat
"""

# 2.Title=Товары ЕАЭС
# 2.1  Товары ЕАЭС		Список
select['eaes_goods_list'] = f"""
  SELECT nn,goods,g33,status,namedoc+' '+ndoc+' '+CONVERT(VARCHAR,datedoc,105) ndoc,packs,ed_izm
    FROM REG_TOV_EA 
    WHERE 1=1 {filter_string_mark}
    ORDER BY nn 
"""

# Title=Изг.товары, сырье
# 3.1  Изг.товары, сырье  Список
select['producted_goods_list'] = f"""
  SELECT nn,goods,g33,status,packs,ed_izm,ndoc,datedoc,goods1,g331,status1,packs1,ed_izm1,ndoc1,datedoc1,guid_cat
    FROM MANF_TOV
    WHERE 1=1 {filter_string_mark}
    ORDER BY nn,status1,datedoc1
"""

# 4.Title=Испол.изг.товаров
# 4.1  Испол.изг.товаров	Список
select['ispol_producted_goods_list'] = f"""
  SELECT nn,goods,g33,packs,ed_izm,treg,status,ndoc,datedoc,ngtd,packs1,ed_izm1,comment
    FROM MANF_TOV_DT 
    WHERE 1=1 {filter_string_mark}
    ORDER BY nn 
"""


def create_select(select, select_name, filters):
    #
    if not filters:
        return select[select_name].replace(filter_string_mark, '')

    filter_substring = str()

    # and datedoc >='"+date1+"' AND datedoc <= '"+date2+"'
    if select_name in ['foreign_goods_list', ]:
        if filters['filterForeignGoodsDateFrom']:
            filter_substring += f"and datebux >='{filters['filterForeignGoodsDateFrom'].replace('-', '')}'"
        if filters['filterForeignGoodsDateTo']:
            filter_substring += f"and datebux <='{filters['filterForeignGoodsDateTo'].replace('-', '')}'"     

    # and datedoc >='"+date1+"' AND datedoc <= '"+date2+"'
    if select_name in ['eaes_goods_list', ]:
        if filters['filterEaesGoodsDateFrom']:
            filter_substring += f"and datedoc >='{filters['filterEaesGoodsDateFrom'].replace('-', '')}'"
        if filters['filterEaesGoodsDateTo']:
            filter_substring += f"and datedoc <='{filters['filterEaesGoodsDateTo'].replace('-', '')}'"   

    # and datedoc >='"+date1+"' AND datedoc <= '"+date2+"'
    if select_name in ['producted_goods_list', ]:
        if filters['filterProductedGoodsDateFrom']:
            filter_substring += f"and datedoc >='{filters['filterProductedGoodsDateFrom'].replace('-', '')}'"
        if filters['filterProductedGoodsDateTo']:
            filter_substring += f"and datedoc <='{filters['filterProductedGoodsDateTo'].replace('-', '')}'" 

    # and datebux >='"+date1+"' AND datebux <= '"+date2+"'
    if select_name in ['ispol_producted_goods_list', ]:
        if filters['filterIspolProductedGoodsDateFrom']:
            filter_substring += f"and datebux >='{filters['filterIspolProductedGoodsDateFrom'].replace('-', '')}'"
        if filters['filterIspolProductedGoodsDateTo']:
            filter_substring += f"and datebux <='{filters['filterIspolProductedGoodsDateTo'].replace('-', '')}'" 


    sql_query = select[select_name].replace(filter_string_mark, filter_substring)
    
    return sql_query



def select_widget_data(select_name, filters):
    #
    with DBConnect() as db:

        query = create_select(select, select_name, filters)
        db.cursor.execute(query)

        # print('description =', db.cursor.description)
        dataset_columns_info = [ (i[0], i[1]) for i in db.cursor.description ]
        # print('dataset_columns_info =', dataset_columns_info)


        dataset = db.cursor.fetchall()
        #print('dataset =', dataset) #

        objects = []
        for data in dataset:

            item = {}
            for i in range(len(dataset_columns_info)):
                item[dataset_columns_info[i][0]] = data[i]
            
            objects.append(item)

        # objects = [
        #     {   
        #         "g33": data[0],
        #         "cnt": data[1],
        #     }
        #     for data in dataset
        # ]

        # print('obj_list =', obj_list)
        # print('objects =', objects)
        
    return objects    


def select_dashboard_data(selects_keys_list=select, filters:Union[dict, None]=None):
    # with DBConnect() as db:
    #     query = """
    #         select * from (
    #         SELECT TOP 7 * FROM
    #             (SELECT LEFT(g33_in,4) g33, count(*) cnt
    #             FROM Luding.dbo.tovar_sklad  WHERE 1=1
    #             GROUP BY LEFT(g33_in,4)) AS a
    #             ORDER BY 2 DESC) b
    #             order by cnt
    #     """
    #     db.cursor.execute(query)
    #     objects = [
    #         {   
    #             "g33": data[0],
    #             "cnt": data[1],
    #         }
    #         for data in db.cursor.fetchall()
    #     ]
    # print('filters = ', filters)

    objects = {}
    for s in selects_keys_list:
        # objects = {'tnved_quantity': select_widget_data('tnved_quantity')}
        objects[s] = select_widget_data(s, filters)
        
    objects['company_name'] = COMPANY_NAME
    objects['current_datetime'] = datetime.now().strftime("%d-%m-%Y %H:%M")

    return objects
