import os
import psycopg2
from eia_fast_app.config.config import config_args

files_to_move_to_pg = ["C:\\Users\\Nikola\\Documents\\GitHub\\Natura2000-Impact_assessment\\data\\Uredba_NN8019_0_Natura.csv",
                       "C:\\Users\\Nikola\\Documents\\GitHub\\Natura2000-Impact_assessment\\data\\Uredba_NN8019_1_Razred.csv",
                       "C:\\Users\\Nikola\\Documents\\GitHub\\Natura2000-Impact_assessment\\data\\Uredba_NN8019_2_Porodica.csv",
                       "C:\\Users\\Nikola\\Documents\\GitHub\\Natura2000-Impact_assessment\\data\\Uredba_NN8019_3_Identifikacijski.csv",
                       "C:\\Users\\Nikola\\Documents\\GitHub\\Natura2000-Impact_assessment\\data\\Uredba_NN8019_4_Identifikacijski.csv"]

class TableCreationQuery():
    def __init__(self, table_name):
        self.table_name = table_name

    def get_creation_string(self.table_name):
        if self.table_name == "Uredba_NN8019_0_Natura":
            create_execute_string = f"""
            CREATE TABLE {table_name}(
            id integer PRIMARY KEY,
            natura_kod text,
            name text,
            cro_name text
            biogeo_region_cont text
            biogeo_region_alpine text
            biogeo_region_med text
            biogeo_region_sea_med text
            )
            """
            return create_execute_string
        
        if self.table_name == "Uredba_NN8019_1_Razred":
            create_execute_string = f"""
            CREATE TABLE {table_name}(
            id integer PRIMARY KEY,
            class text,
            order text,
            family text,
            name_by_directive text
            name text
            cro_name text
            biogeo_region_cont text
            biogeo_region_alpine text
            biogeo_region_med text
            biogeo_region_sea_med text
            )
            """
            return create_execute_string
        
        if self.table_name == "Uredba_NN8019_2_Porodica":
            create_execute_string = f"""
            CREATE TABLE {table_name}(
            id integer PRIMARY KEY,
            family text,
            name text
            cro_name text
            status text
            category text
            )
            """
            return create_execute_string
        
        if self.table_name == "Uredba_NN8019_3_Identifikacijski":
            create_execute_string = f"""
            CREATE TABLE {table_name}(
            id integer PRIMARY KEY,
            sitecode text,
            sitename text
            category text
            name text
            cro_name text
            status_g text
            status_p text
            status_z text
            )
            """
            return create_execute_string
        
        if self.table_name == "Uredba_NN8019_4_Identifikacijski":
            create_execute_string = f"""
            CREATE TABLE {table_name}(
            id integer PRIMARY KEY,
            sitecode text,
            sitename text
            category text
            cro_name text
            name text
            )
            """
            return create_execute_string



with psycopg2.connect(**config_args, options = "-c search_path=data, public") as conn:
    with conn.cursor() as cur:
        for i in files_to_move_to_pg:
            table_name = os.path.basename(i)
            table_name = table_name.split(".")[0]

            new_query = TableCreationQuery(table_name)
            create_execute_string = new_query.get_creation_string()

            cur.execute(create_execute_string)
            
            with open(i, 'r', encoding="utf-8") as f:
                next(f) # Skip the header row.
                cur.copy_from(f, table_name, sep=',')

conn.commit()