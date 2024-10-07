# ETL Pipeline using Databricks & AWS S3

This project demonstrates an ETL pipeline using PySpark on Databricks, reading and writing data to AWS S3.

## Setup Instructions

### Step 1: Set Up AWS S3
1. **Create an S3 bucket**:
   - Go to AWS Management Console → S3 → Create Bucket.
   - Provide a unique name (e.g., `databricks-etl-pipeline-bucket`) and configure necessary permissions and region.
   
2. **Upload the input file**:
   - In the S3 bucket, upload a sample CSV file (e.g., `input_data.csv`).

### Step 2: Configure Databricks
1. **Create a Databricks Cluster**:
   - Login to your Databricks workspace and navigate to the Clusters page.
   - Click **Create Cluster**, select the runtime version (ensure it supports PySpark), and start the cluster.

2. **Upload the ETL Script**:
   - Navigate to the **Workspace** section → Create a new **Notebook**.
   - Copy the content from `etl_pipeline.py` into the notebook.

3. **Configure AWS Credentials in Databricks**:
   - Use Databricks secrets or environment variables to set your AWS access keys securely.
   - Example:
     ```python
     spark.conf.set("fs.s3a.access.key", "<Your_AWS_Access_Key>")
     spark.conf.set("fs.s3a.secret.key", "<Your_AWS_Secret_Key>")
     ```

### Step 3: Run the Script
1. **Update S3 paths** in the ETL script:
   - Ensure that `input_path` and `output_path` point to your S3 bucket.
   
2. **Run the ETL script** on Databricks.

---

## Python Code (`etl_pipeline.py`):
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
