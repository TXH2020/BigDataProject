import os
from pyspark.sql import SparkSession
os.environ['PYSPARK_SUBMIT_ARGS'] = "--packages com.datastax.spark:spark-cassandra-connector_2.12:3.2.0 pyspark-shell"
spark = SparkSession.builder.getOrCreate()
spark.conf.set(r"spark.sql.catalog.mycatalog", "com.datastax.spark.connector.datasource.CassandraCatalog")
spark.read.table("mycatalog.chat_keyspace.chat_table").show()
spark.stop()