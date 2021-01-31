import pandas as pd
from pandas.io.json import json_normalize

import api_request
import make_tables
import os


class ETL:

    def __init__(self, offset=[0], with_drop_table=True):
        self.with_drop_table = with_drop_table
        self.offset = offset
        self.cursor, self.connection = make_tables.connect_to_database()

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
                "review_count",
                "rating",
                "phone",
                "distance",
                ["coordinates", "latitude"],
                ["coordinates", "longitude"],
                ["location", "zip_code"]]
        meta_prefix = "restaurant_"
        record_prefix = "category_"

        df_list = []
        for each in self.data:
            df_list.append(json_normalize(each['businesses'], sep="_",
                                          record_path=record_path,
                                          meta=meta,
                                          meta_prefix=meta_prefix,
                                          record_prefix=record_prefix))

        self.final_df = pd.concat(df_list, ignore_index=True)
        print("Final data frame created...")
        print(self.final_df.info())
        print(self.final_df.head())

    def load(self):

        self.final_df.to_sql(
            name="RAW_TABLE",
            schema="public",
            con=self.connection,
            if_exists="append",
            index=False)

        make_tables.close_connection()


if __name__ == "__main__":
    etl = ETL(offset=list(range(0, 100, 10)))
    etl.extract_data()
    etl.transform_data()
    etl.load()
