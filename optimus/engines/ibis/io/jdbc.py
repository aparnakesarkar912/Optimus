import ibis

from optimus.engines.base.contants import LIMIT_TABLE
from optimus.engines.base.dask.io.jdbc import DaskBaseJDBC
from optimus.helpers.converter import dask_dataframe_to_dask_cudf


class JDBC(DaskBaseJDBC):
    def __init__(self, host, database, user, password, port=None, driver=None, schema="public", oracle_tns=None,
                 oracle_service_name=None, oracle_sid=None, presto_catalog=None, cassandra_keyspace=None,
                 cassandra_table=None, bigquery_project=None, bigquery_dataset=None):
        super().__init__(host, database, user, password, port=port, driver=driver, schema=schema,
                         oracle_tns=oracle_tns,
                         oracle_service_name=oracle_service_name, oracle_sid=oracle_sid,
                         presto_catalog=presto_catalog,
                         cassandra_keyspace=cassandra_keyspace,
                         cassandra_table=cassandra_table)

    def tables(self, schema=None, database=None, limit=None):
        con = ibis.mysql.connect(url=self.uri)
        return con.list_tables()

    def table_to_df(self, table_name, columns="*", limit=None):
        con = ibis.mysql.connect(url=self.uri)
        print(table_name, LIMIT_TABLE, self.uri)
        return con.table(table_name)


        # return dask_dataframe_to_dask_cudf(super().table_to_df(table_name, columns, limit))

    # def execute(self, query, limit=None, num_partitions: int = NUM_PARTITIONS, partition_column: str = None,
    #             table_name=None):
    #     return super().execute(query, limit, num_partitions, partition_column, table_name).compute()
