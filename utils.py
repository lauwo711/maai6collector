import boto3
import logging


# log format
DEFAULT_LOGGING_FORMAT = "[%(asctime)s]:[%(levelname)s]: (%(name)s:%(threadName)-10s/%(process)d) %(message)s"

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=DEFAULT_LOGGING_FORMAT)


class Storage:
    def __new__(cls, full_path, **kwargs):
        if full_path.startswith("S3://"):
            return S3Client(full_path, **kwargs)
        elif full_path.startswith("C:/"):
            return LocalClient(full_path)
        else:
            logger.error("Cannot recognize storage path.")


class LocalClient:
    def __init__(self, full_path):
        self.full_path = full_path

    def save_df(self, df, path, index=False, to_format="csv"):
        final_path = f"{self.full_path}{path}"
        match to_format:
            case "csv":
                df.to_csv(final_path, index=index)
            case "parquet":
                df.to_parquet(final_path, index=index)
        logger.info(f"File saved locally: {self.full_path}{path}")
        return


class S3Client:
    def __init__(self, full_path, **kwargs):
        self.s3c = boto3.client(service_name="s3", **kwargs)
        self.full_path = full_path
        self.bucket = full_path.split("S3://")[1].split("/")[0]
        self.key = full_path.split("S3://")[1].split(f"{self.bucket}/")[1]

    def save_df(self, df, path, index=False, to_format="csv"):
        match to_format:
            case "csv":
                data = df.to_csv(index=index)
            case "parquet":
                data = df.to_parquet(index=index)
            case _:
                logger.error("This format is not allowed.")
                return
        r = self.s3c.put_object(Bucket=self.bucket, Key=f"{self.key}{path}", Body=data)
        if r["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logger.info(f"File saved on: {self.full_path}{path}")
        else:
            logger.error(f"File SAVING ERROR on s3: {self.full_path}{path}")
        return
