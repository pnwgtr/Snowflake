from snowflake.snowpark import Session
from snowflake.snowpark.functions import udf
from snowflake.snowpark.types import (
    FloatType, StringType,
    StructType, StructField
)

from utils import calculate_cyber_risk_metrics

# Connect to Snowflake
connection_parameters = {
    "account": "<your_account>",
    "user": "<your_username>",
    "password": "<your_password>",
    "role": "<your_role>",
    "warehouse": "<your_warehouse>",
    "database": "<your_database>",
    "schema": "<your_schema>"
}

session = Session.builder.configs(connection_parameters).create()

# Define output schema
output_schema = StructType([
    StructField("SLE", FloatType()),
    StructField("ALE_BEFORE", FloatType()),
    StructField("ALE_AFTER", FloatType()),
    StructField("RISK_REDUCTION", FloatType()),
    StructField("ROI", FloatType())
])

# Register the UDF
@udf(
    input_types=[
        FloatType(), FloatType(), FloatType(), FloatType(),
        FloatType(), FloatType(), FloatType(),
        FloatType(), FloatType(), StringType()
    ],
    return_type=output_schema,
    name="CYBER_RISK_METRICS",
    replace=True
)
def cyber_risk_metrics_udf(
    controls_cost, revenue, user_count, monitoring_cost_per_user,
    base_sle, downtime_days, cost_per_day,
    aro_before_percent, aro_after_percent, maturity_level
):
    return calculate_cyber_risk_metrics(
        controls_cost, revenue, user_count, monitoring_cost_per_user,
        base_sle, downtime_days, cost_per_day,
        aro_before_percent, aro_after_percent, maturity_level
    )

print("UDF registered successfully.")
