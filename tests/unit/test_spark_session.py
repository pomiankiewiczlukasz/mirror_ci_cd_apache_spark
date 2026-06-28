from pyspark.sql import SparkSession

from us_accidents_etl.config.settings import SparkConfig
from us_accidents_etl.spark.session import create_spark_session


def test_create_spark_session_returns_spark_session():
    cfg = SparkConfig(master="local[1]", app_name="test-create-session")
    session = create_spark_session(cfg)
    assert isinstance(session, SparkSession)


def test_create_spark_session_is_usable():
    cfg = SparkConfig(master="local[1]")
    session = create_spark_session(cfg)
    df = session.createDataFrame([(1,)], ["x"])
    assert df.count() == 1
