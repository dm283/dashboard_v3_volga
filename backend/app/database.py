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



# # 1.Title=Артикулы Своб.склада
# # 1.1  Количество ДТ на складе	Число
# select['articul_dt_cnt'] = f"""
#   SELECT count(DISTINCT ngtd) articul_dt_cnt FROM {DB_NAME}.{DB_SCHEMA}.reg_curdet
# """

# # 1.2  Кол-во артикула на складе		Число	
# select['articul_articul_cnt'] = f"""
#   SELECT  count(*) articul_articul_cnt FROM {DB_NAME}.{DB_SCHEMA}.reg_curdet
# """

# # 1.3  ТНВЭД на складе			Столбиковая диаграмма (горизонтальная ?)
# select['articul_tnved'] = f"""
#   SELECT TOP 7 * FROM
#     (SELECT  LEFT(g33,4) g33, count(*) cnt 
#     FROM {DB_NAME}.{DB_SCHEMA}.reg_curdet WHERE 1=1
#     GROUP BY LEFT(g33,4)) AS a
#     ORDER BY 2 DESC
# """

# # 1.4 Артикул на складе			Список
# select['articul_articul'] = f"""
#   SELECT ngtd,date,catalog,packs,unit,name,status,g33,g32,netto,cell_id,guid_cat 
#     FROM {DB_NAME}.{DB_SCHEMA}.reg_curdet 
#     ORDER BY date,ngtd,catalog
# """


# # 2.Title=Приход товара
# # 2.1  Количество принятого товара 	Число
# select['arrival_goods_cnt'] = f"""
#   SELECT count(*) arrival_goods_cnt FROM {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar
#     WHERE 1=1 {filter_string_mark}
# """

# # 2.2  Количество принятых ДТ(77)		Число
# select['arrival_dt_cnt'] = f"""
#   SELECT count(DISTINCT ngtd) arrival_dt_cnt FROM {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar
#     WHERE 1=1 {filter_string_mark}
# """

# # 2.3  Принятые ТНВЭД (7)			Столбиковая диаграмма
# select['arrival_tnved'] = f"""
#   SELECT TOP 7 * FROM
#     (SELECT  LEFT(g33,4) g33, count(*) cnt 
#     FROM {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar WHERE 1=1 {filter_string_mark}
#     GROUP BY LEFT(g33,4)) AS a
#     ORDER BY 2 DESC
# """

# # 2.4  Приход  товара		Список
# select['arrival_goods_arrival'] = f"""
#   SELECT date,ngtd,status,cell_id,g32,g31,g33,g31_4,g41a,netto,brutto,sub_id
#     FROM {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar 
#     WHERE 1=1 {filter_string_mark}
#     ORDER BY ngtd,g32 
# """

# # 3.Title=Движение товара
# # 3.1  Движение товара по складу		Список
# select['goods_movement'] = f"""
# SELECT t.ngtd,t.status,t.g32,t.g31,t.g33,t.g41,
# CASE WHEN t.g41a<>'166' THEN h.pin ELSE 0 END pin,
# CASE WHEN t.g41a<>'166' THEN h.pout ELSE 0 END pout,
# h.g38in,h.g38out 
# FROM {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar t INNER JOIN 
# (SELECT op,t.sub_id,sum(packs_in) pin,sum(packs_out) pout,sum(g38_in) g38in,sum(g38_out) g38out
# 		FROM ({DB_NAME}.{DB_SCHEMA}.reg_histdet h INNER JOIN {DB_NAME}.{DB_SCHEMA}.decl_priem_articul s ON s.guid_cat=h.guid_cat) 
#  		LEFT OUTER JOIN {DB_NAME}.{DB_SCHEMA}.decl_priem_tovar t ON s.sub_id=t.sub_id 
# 		WHERE 1=1 {filter_string_mark}
# 		GROUP BY t.sub_id,op) h ON t.sub_id=h.sub_id WHERE h.pin-h.pout > 0
# """

######### old
# select['product_quantity'] = f"""
#   SELECT count(*) product_quantity FROM {DB_NAME}.{DB_SCHEMA}.tovar_sklad
# """

# select['dt_quantity'] = f"""
#   SELECT count(*) dt_quantity FROM (SELECT id_doc FROM {DB_NAME}.{DB_SCHEMA}.tovar_sklad GROUP BY id_doc) AS a
# """

# select['tnved_quantity'] = f"""
#             select * from (
#             SELECT TOP 7 * FROM
#                 (SELECT LEFT(g33_in,4) g33, count(*) cnt
#                 FROM {DB_NAME}.{DB_SCHEMA}.tovar_sklad  WHERE 1=1
#                 GROUP BY LEFT(g33_in,4)) AS a
#                 ORDER BY 2 DESC) b
#                 order by cnt desc
#         """

# select['products_on_storage'] = f"""
#   SELECT id,gtdnum,name, cast(date_in as date) date_in, g32,g31,g33_in,g31_2,
#   CASE WHEN g41a <>'166' THEN g31_3 ELSE 0 END g31_3,
#   CASE WHEN g41a <>'166' THEN g31_3a ELSE '' END g31_3a,
#   g35,g41a, cast(date_chk as date) date_chk, country 
#   FROM {DB_NAME}.{DB_SCHEMA}.TOVAR_SKLAD 
#   ORDER BY date_in ASC,gtdnum,g32
# """

# #########################
# filter_string_mark = '!filter_string_mark!'

# select['received_product_quantity'] = f"""
#   SELECT count(*) received_product_quantity
#     FROM {DB_NAME}.{DB_SCHEMA}.doc_in_sklad d, {DB_NAME}.{DB_SCHEMA}.doc_in_sklad_sub s 
#     WHERE s.main_id=d.id AND d.posted > 0
#     {filter_string_mark}
    
# """
# # {dashboard_filter_string}
# # select_filter[s5] = list()
# # select_filter[s5].append("and d.date_doc >='dashboard_filter_0_0'")
# # select_filter[s5].append("and d.date_doc <= 'dashboard_filter_0_1'")


# select['received_dt_quantity'] = f"""
#   SELECT count(*) received_dt_quantity
#     FROM {DB_NAME}.{DB_SCHEMA}.doc_in_sklad d
#     WHERE posted > 0
#     {filter_string_mark}
# """
# # {dashboard_filter_string}
# # select_filter[s6] = list()
# # select_filter[s6].append("and d.date_doc >='dashboard_filter_0_0'")
# # select_filter[s6].append("and d.date_doc <= 'dashboard_filter_0_1'")


# select['received_tnved_quantity'] = f"""
#   SELECT TOP 7 * FROM
#   (SELECT  LEFT(s.g33_in,4) g33, count(*) cnt 
#     FROM {DB_NAME}.{DB_SCHEMA}.doc_in_sklad_sub s, {DB_NAME}.{DB_SCHEMA}.doc_in_sklad d  
#     where s.main_id=d.id AND d.posted > 0
#     {filter_string_mark}
#     GROUP BY LEFT(s.g33_in,4)) AS a
#   ORDER BY 2 DESC
# """
# # select_filter[s7] = list()
# # select_filter[s7].append("and d.date_doc >='dashboard_filter_0_0'")
# # select_filter[s7].append("and d.date_doc <= 'dashboard_filter_0_1'")


# select['account_book'] = f"""
#   SELECT * FROM 
#   (SELECT UniqueIndexField as id, id as id_0, f_p,name,gtdnum, cast(date_in as date) date_in, time_in,
#   cast(date_otc as date) date_otc, cast(date_chk as date) date_chk, g32,g31,g33_in,g35,
#   CASE WHEN g31_3a <>'КГ' THEN g31_3 ELSE 0 END g31_3,
#   CASE WHEN g31_3a <>'КГ' THEN g31_3a ELSE '' END g31_3a,
#   doc_num_out, gtdregime_out, cast(date_out as date) date_out, g32_out, g33_out, g31_2_out, g35_out,
#   CASE WHEN g31_3a <>'КГ' THEN g31_3_out ELSE 0 END g31_3_out
#   FROM {DB_NAME}.{DB_SCHEMA}.jr_sklad ) AS a
#   where 1=1
#   {filter_string_mark}
#   ORDER BY date_in,id ASC,g32 ASC,f_p DESC,date_otc ASC
# """
# # select_filter[s8] = list()
# # select_filter[s8].append("and date_in >='dashboard_filter_1_0'")
# # select_filter[s8].append("and date_in <= 'dashboard_filter_1_1'")


# select['report_vehicle'] = f"""
# SELECT nn as id, gtdnum,g32,g33_in,g31,
# CAST(g35 AS NUMERIC(18,3)) g35,
# g31_3a,place,gtdregime_out,doc_num_out,g33_out,
# CAST(g35_out AS NUMERIC(18,3)) g35_out,
# CASE WHEN g31_3a <> 'КГ' THEN CAST(CAST(g31_3 AS NUMERIC(18,3)) AS VARCHAR)+'/'+g31_3a ELSE '0' END g31_3, 
# CASE WHEN g31_3a <> 'КГ' THEN CAST(CAST(g31_3_out AS NUMERIC(18,3)) AS VARCHAR)+'/'+g31_3a ELSE '0' END g31_3_out, 
# CONVERT(VARCHAR,date_in,105) AS date_in,
# CONVERT(VARCHAR,date_chk,105) AS date_chk,
# CASE WHEN exp_date IS NOT NULL THEN CONVERT(VARCHAR,exp_date,105) ELSE 'ОТСУТСТВУЕТ' END AS exp_date,
# CONVERT(VARCHAR,date_out,105) AS date_out,
# CASE WHEN g31_3ost>0 THEN CAST(g35ost AS NUMERIC(18,3)) ELSE 0 END g35ost_,
# CASE WHEN g31_3a <> 'КГ' THEN CAST(CAST(g31_3ost AS NUMERIC(18,3)) AS VARCHAR)+'/'+g31_3a ELSE '0' END g31_3ost_ 
# FROM (SELECT CONVERT(INTEGER,row_number() OVER( ORDER BY j.date_in,j.id,j.g32,j.key_id,jj.date_out)) nn,j.*,
#    jj.date_out,jj.doc_num_out,jj.gtdregime_out,
#    jj.g35_out,jj.g31_3_out,jj.g31_3a_out,jj.g31_out,jj.g32_out,jj.g33_out,j.g31_3-ISNULL(jjj.g31_3sout,0) g31_3ost,
#    g35-ISNULL(jjj.g35sout,0) g35ost 
# FROM (SELECT j.id,j.key_id,j.g32,j.gtdnum,j.date_in,j.g31,j.g31_3,j.g31_3a,j.g33_in,j.g35,j.gtdregime_in,j.date_chk,
#    j.place,s.exp_date,s.g41a_dt,u.code 
# FROM ({DB_NAME}.{DB_SCHEMA}.jr_sklad j LEFT OUTER JOIN {DB_NAME}.{DB_SCHEMA}.units u ON u.name10=j.g31_3a) 
# LEFT OUTER JOIN {DB_NAME}.{DB_SCHEMA}.doc_in_sklad_sub s ON s.key_id=j.key_id 
# WHERE f_p='1' 
# {filter_string_mark}
# ) 
# j LEFT OUTER JOIN (SELECT key_id,sum(g35_out) 
#    g35sout,sum(g31_3_out) g31_3sout 
# FROM {DB_NAME}.{DB_SCHEMA}.jr_sklad jj WHERE f_p='0' GROUP BY key_id ) jjj ON jjj.key_id=j.key_id 
# LEFT OUTER JOIN (SELECT key_id,doc_num_out,gtdregime_out,date_out,g31_3_out,g31_3a_out,g35_out,g31_out,g32_out,g33_out 
# FROM {DB_NAME}.{DB_SCHEMA}.jr_sklad WHERE  f_p='0') jj  ON j.key_id=jj.key_id ) AS a WHERE 1=1
# ORDER BY nn
# """
# # select_filter[s9] = list()
# # select_filter[s9].append("and date_out >='dashboard_filter_2_0'")
# # select_filter[s9].append("and date_in <= 'dashboard_filter_2_1'")


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


# old
    # # and date >='"+date1+"' AND date <= '"+date2+"'
    # if select_name in ['arrival_goods_cnt', 'arrival_dt_cnt', 'arrival_tnved', 'arrival_goods_arrival',]:
    #     if filters['filterArrivalDateFrom']:
    #         filter_substring += f"and date >='{filters['filterArrivalDateFrom'].replace('-', '')}'"
    #     if filters['filterArrivalDateTo']:
    #         filter_substring += f"and date <='{filters['filterArrivalDateTo'].replace('-', '')}'"    

    # # and h.date_op >='"+date1+"' AND h.date_op <= '"+date2+"'  
    # if select_name in ['goods_movement',]:
    #     if filters['filterGoodsMovementDateOpFrom']:
    #         filter_substring += f"and h.date_op >='{filters['filterGoodsMovementDateOpFrom'].replace('-', '')}'"
    #     if filters['filterGoodsMovementDateOpTo']:
    #         filter_substring += f"and h.date_op <='{filters['filterGoodsMovementDateOpTo'].replace('-', '')}'"   

################################### old
    # # and d.date_doc >='dashboard_filter_0_0' and d.date_doc <= 'dashboard_filter_0_1'
    # if select_name in ['received_product_quantity', 'received_dt_quantity', 'received_tnved_quantity']:
    #     if filters['filterAccountBookDateDocFrom']:
    #         filter_substring += f"and d.date_doc >='{filters['filterAccountBookDateDocFrom'].replace('-', '')}'"
    #     if filters['filterAccountBookDateDocTo']:
    #         filter_substring += f"and d.date_doc <='{filters['filterAccountBookDateDocTo'].replace('-', '')}'"

    # # and date_in >='dashboard_filter_1_0' and date_in <= 'dashboard_filter_1_1'
    # if select_name in ['account_book']:
    #     if filters['filterAccountBookDateEnterFrom']:
    #         filter_substring += f"and date_in >='{filters['filterAccountBookDateEnterFrom'].replace('-', '')}'"
    #     if filters['filterAccountBookDateEnterTo']:
    #         filter_substring += f"and date_in <='{filters['filterAccountBookDateEnterTo'].replace('-', '')}'"

    # # and date_out >='dashboard_filter_2_0' and date_in <= 'dashboard_filter_2_1'
    # if select_name in ['report_vehicle']:
    #     if filters['filterReportVehicleDateEnterFrom']:
    #         filter_substring += f"and date_out >='{filters['filterReportVehicleDateEnterFrom'].replace('-', '')}'"
    #     if filters['filterReportVehicleDateExitTo']:
    #         filter_substring += f"and date_in <='{filters['filterReportVehicleDateExitTo'].replace('-', '')}'"

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
