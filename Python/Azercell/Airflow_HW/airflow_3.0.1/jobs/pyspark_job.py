from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("airflow-test-job").getOrCreate()

data = [("Alice", 1), ("Bob", 2), ("Charlie", 3)]
df = spark.createDataFrame(data, ["name", "value"])
df.show()

df.write.mode("overwrite").csv("/opt/spark-data/output")

spark.stop()
