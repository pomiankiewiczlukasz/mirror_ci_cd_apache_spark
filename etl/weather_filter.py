from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def filter_high_severity(df: DataFrame, cfg):
    return df.filter(F.col("Severity") >= cfg.min_severity)

def filter_weather_conditions(df: DataFrame, cfg):
    return df.filter(
        F.col("Weather_Condition").isin(cfg.weather_conditions)
    )

def apply_etl_filters(df: DataFrame, cfg):
    return (
        filter_high_severity(df, cfg)
        .transform(lambda d: filter_weather_conditions(d, cfg))
    )