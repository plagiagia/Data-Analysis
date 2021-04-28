import os

import pandas as pd
from pandas import json_normalize
from sqlalchemy import create_engine

import api_request
import make_tables


class ETL:

    def __init__(self, offset=[0], with_drop_table=True):
        self.with_drop_table = with_drop_table
        self.offset = offset
        self.cursor, self.connection = make_tables.connect_to_database()
        self.data = None
        self.final_df = None

        if self.with_drop_table:
            make_tables.drop_tables(self.cursor, self.connection)

        make_tables.create_tables(self.cursor, self.connection)
        print("All tables are initialized...")

    def extract_data(self):
        print("Extract data from the API...")
        self.data = api_request.get_response(offset=self.offset)

    def transform_data(self):
        record_path = "categories"
        meta = ["id",
                "name",
                "price",
                "review_count",
                "rating",
                "phone",
                "distance",
                ["coordinates", "latitude"],
                ["coordinates", "longitude"],
                ["location", "zip_code"],
                ["location", "address1"]]
        meta_prefix = "restaurant_"
        record_prefix = "category_"

        df_list = []
        for each in self.data:
            df_list.append(json_normalize(each['businesses'], sep="_",
                                          record_path=record_path,
                                          meta=meta,
                                          errors='ignore',
                                          meta_prefix=meta_prefix,
                                          record_prefix=record_prefix))

        self.final_df = pd.concat(df_list, ignore_index=True)
        print("Final data frame created...")
        print(self.final_df.info())

    def load(self):

        # Save DF to a CSV file locally
        self.final_df.to_csv('./tmp_df.csv', header=True, index_label='id', index=True, encoding='utf-8')

        # Make a connection with the SQLalchemy package
        connect = "postgresql+psycopg2://%s:%s@%s:5432/%s" % (
            os.environ.get("DB_USER"),
            os.environ.get("DB_PASSWORD"),
            os.environ.get("HOST"),
            os.environ.get('DATABASE_NAME')
        )
        # Create engine
        engine = create_engine(connect)

        self.final_df.to_sql(
            name="RAW_TABLE",
            con=engine,
            if_exists="replace",
            index=True)

        make_tables.close_connection(conn=self.connection)


if __name__ == "__main__":
    etl = ETL(offset=list(range(0, 100, 10)))
    etl.extract_data()
    etl.transform_data()
    etl.load()
