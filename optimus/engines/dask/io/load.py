import ntpath

import dask.bag as db
import pandas as pd
from dask import dataframe as dd

from optimus.helpers.functions import prepare_path
from optimus.helpers.logger import logger


class Load:

    @staticmethod
    def json(path, multiline=False, *args, **kwargs):
        """
        Return a dask dataframe from a json file.
        :param path: path or location of the file.
        :param multiline:

        :return:
        """
        file, file_name = prepare_path(path, "json")

        try:
            # TODO: Check a better way to handle this Spark.instance.spark. Very verbose.
            df = dd.read_json(path, lines=multiline, *args, **kwargs)
            df.meta.set("file_name", file_name)

        except IOError as error:
            logger.print(error)
            raise
        return df

    @staticmethod
    def tsv(path, header=True, infer_schema=True, *args, **kwargs):
        """
        Return a spark from a tsv file.
        :param path: path or location of the file.
        :param header: tell the function whether dataset has a header row. True default.
        :param infer_schema: infers the input schema automatically from data.
        It requires one extra pass over the data. True default.

        :return:
        """

        return Load.csv(path, sep='\t', header=header, infer_schema=infer_schema, *args, **kwargs)

    @staticmethod
    def csv(path, sep=',', header=True, infer_schema=True, charset="UTF-8", null_value="None", n_rows=-1, cache=False,
            *args,
            **kwargs):
        """
        Return a dataframe from a csv file. It is the same read.csv Spark function with some predefined
        params

        :param path: path or location of the file.
        :param sep: usually delimiter mark are ',' or ';'.
        :param header: tell the function whether dataset has a header row. True default.
        :param infer_schema: infers the input schema automatically from data.
        :param charset:
        :param null_value:
        :param n_rows:
        :param cache: If calling from a url we cache save the path to the temp file so we do not need to download the file again

        """

        if cache is False:
            prepare_path.cache_clear()

        file, file_name = prepare_path(path, "csv")
        try:
            df = dd.read_csv(file, sep=sep, header=0 if header else None, encoding=charset, na_values=null_value, *args,
                             **kwargs)
            if n_rows > -1:
                df = df.head(n_rows)

            df.meta.set("file_name", file_name)
        except IOError as error:
            logger.print(error)
            raise
        df.ext.reset()
        return df

    @staticmethod
    def parquet(path, columns=None, *args, **kwargs):
        """
        Return a spark from a parquet file.
        :param path: path or location of the file. Must be string dataType
        :param columns: select the columns that will be loaded. In this way you do not need to load all the dataframe
        :param args: custom argument to be passed to the spark parquet function
        :param kwargs: custom keyword arguments to be passed to the spark parquet function
        :return: Spark Dataframe
        """

        file, file_name = prepare_path(path, "parquet")

        try:
            df = dd.read_parquet(path, columns=columns, engine='pyarrow', *args, **kwargs)
            df.meta.set("file_name", file_name)

        except IOError as error:
            logger.print(error)
            raise

        return df

    @staticmethod
    def zip(path, sep=',', header=True, infer_schema=True, charset="UTF-8", null_value="None", n_rows=-1, *args,
            **kwargs):
        file, file_name = prepare_path(path, "zip")

        from zipfile import ZipFile
        import dask.dataframe as dd
        import os

        wd = '/path/to/zip/files'
        file_list = os.listdir(wd)
        destdir = '/extracted/destination/'

        ddf = dd.from_pandas(pd.DataFrame())

        for f in file_list:
            with ZipFile(wd + f, "r") as zip:
                print(zip.namelist())
                zip.extractall(destdir, None, None)
                df = dd.read_csv(zip.namelist(), usecols=['Enter', 'Columns', 'Here'], parse_dates=['Date'])
                ddf = ddf.append(df)

        ddf.compute()

        # print("---",path, file, file_name)
        try:
            df = dd.read_csv(file, sep=sep, header=0 if header else None, encoding=charset, na_values=null_value,
                             compression="gzip", *args,
                             **kwargs)

            if n_rows > -1:
                df = df.head(n_rows)

            df.meta.set("file_name", file_name)
        except IOError as error:
            logger.print(error)
            raise
        df.ext.reset()
        return df

    @staticmethod
    def avro(path, *args, **kwargs):
        """
        Return a spark from a avro file.
        :param path: path or location of the file. Must be string dataType
        :param args: custom argument to be passed to the spark avro function
        :param kwargs: custom keyword arguments to be passed to the spark avro function
        :return: Spark Dataframe
        """
        file, file_name = prepare_path(path, "avro")

        try:
            df = db.read_avro(path, *args, **kwargs).to_dataframe()
            df.meta.set("file_name", file_name)

        except IOError as error:
            logger.print(error)
            raise

        return df

    @staticmethod
    def excel(path, sheet_name=0, *args, **kwargs):
        """
        Return a spark from a excel file.
        :param path: Path or location of the file. Must be string dataType
        :param sheet_name: excel sheet name
        :param args: custom argument to be passed to the excel function
        :param kwargs: custom keyword arguments to be passed to the excel function
        :return: Spark Dataframe
        """
        file, file_name = prepare_path(path, "xls")

        try:
            pdf = pd.read_excel(file, sheet_name=sheet_name, *args, **kwargs)

            # Parse object column data type to string to ensure that Spark can handle it. With this we try to reduce
            # exception when Spark try to infer the column data type
            col_names = list(pdf.select_dtypes(include=['object']))

            column_dtype = {}
            for col in col_names:
                column_dtype[col] = str

            # Convert object columns to string
            pdf = pdf.astype(column_dtype)

            # Create spark data frame
            df = dd.from_pandas(pdf, npartitions=3)
            df.meta.set("file_name", ntpath.basename(file_name))
        except IOError as error:
            logger.print(error)
            raise

        return df