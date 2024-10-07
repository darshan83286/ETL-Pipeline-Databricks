
### 2. **`ETL-Pipeline-Databricks/etl_pipeline.py`**

```python
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Initialize Spark session
spark = SparkSession.builder \
    .appName("ETL Pipeline with Databricks & S3") \
    .getOrCreate()

# Define S3 paths
input_path = "s3a://databricks-etl-pipeline-bucket/input_data.csv"
output_path = "s3a://databricks-etl-pipeline-bucket/output_data/"

# Step 1: Extract - Load data from S3
print("Extracting data from S3...")
df = spark.read.csv(input_path, header=True, inferSchema=True)

# Step 2: Transform - Apply transformations (e.g., filtering, calculating)
print("Transforming data...")
transformed_df = df.filter(col("salary") > 55000) \
                   .withColumnRenamed("name", "employee_name")

# Step 3: Load - Save the transformed data back to S3
print("Loading transformed data to S3...")
transformed_df.write.mode("overwrite").parquet(output_path)

print("ETL pipeline completed successfully!")
