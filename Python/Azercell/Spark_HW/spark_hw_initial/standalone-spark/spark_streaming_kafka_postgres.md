# Spark Streaming: Kafka → PostgreSQL

This pipeline reads messages from Kafka, processes them with Spark Structured Streaming, and writes the results to a PostgreSQL database using `foreachBatch`.

---

## 1. Read from Kafka
- Initialize a Spark session with Kafka support.
- Configure the Kafka bootstrap servers and topic(s).
- Read the stream as a DataFrame.

---

## 2. Process the Data
- Parse the Kafka message `key` and `value` fields.
- Apply necessary transformations:
  - Deserialize JSON/Avro (if applicable).
  - Cast columns to appropriate types.
  - Filter, aggregate, or enrich data.

---

## 3. Write to PostgreSQL (foreachBatch)
- Use `foreachBatch` to handle each micro-batch.
- Inside the batch function:
  - Open a JDBC connection to PostgreSQL.
  - Write the DataFrame in **append** mode.
  - Handle transaction management or error handling as needed.

---

## 4. Start the Stream
- Define the checkpoint location for fault tolerance.
- Start the query.
- Await termination to keep the stream running.

---

## Notes
- Ensure PostgreSQL JDBC driver is available in Spark (`--jars` option).
- Use `checkpointLocation` for recovery.
- Tune batch size and parallelism for throughput.
