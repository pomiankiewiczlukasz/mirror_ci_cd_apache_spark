from unittest.mock import patch

from pyspark.sql import SparkSession

from us_accidents_etl.config.settings import ETLConfig, Settings, SparkConfig
from us_accidents_etl.pipeline import run


def _make_settings(output_path: str | None = None) -> Settings:
    return Settings.model_construct(
        spark=SparkConfig(),
        etl=ETLConfig(
            input_path="gs://dummy/input",
            output_path=output_path,
            min_severity=2,
            weather_conditions=["Rain", "Snow"],
        ),
    )


def _make_raw_df(spark: SparkSession):
    data = [
        (2, "Rain", "Miami", "FL", "Day", "2021-01-01 08:00:00", "2021-01-01 08:30:00"),
        (
            3,
            "Snow",
            "Austin",
            "TX",
            "Night",
            "2021-01-02 14:00:00",
            "2021-01-02 14:20:00",
        ),
        (
            4,
            "Rain",
            "Los Angeles",
            "CA",
            "Day",
            "2021-01-03 09:00:00",
            "2021-01-03 09:15:00",
        ),
    ]
    return spark.createDataFrame(
        data,
        [
            "Severity",
            "Weather_Condition",
            "City",
            "State",
            "Sunrise_Sunset",
            "Start_Time",
            "End_Time",
        ],
    )


def test_run_without_ml(spark: SparkSession, tmp_path):
    raw_df = _make_raw_df(spark)
    settings = _make_settings(str(tmp_path / "out"))

    with (
        patch("us_accidents_etl.pipeline.read_accidents_csv", return_value=raw_df),
        patch("us_accidents_etl.pipeline.write_filtered") as mock_filtered,
        patch("us_accidents_etl.pipeline.write_aggregations") as mock_agg,
    ):
        run(spark, settings)

    mock_filtered.assert_called_once()
    mock_agg.assert_called_once()
