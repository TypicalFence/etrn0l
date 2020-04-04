from typing import Optional
from botocore.exceptions import ClientError  # type: ignore
from kyasshu import Cache, DummyBackend  # type: ignore
from . import FlashFileService


class S3FlashFileService(FlashFileService):

    def __init__(self, s3_client,
                 bucket_name: str, cache: Optional[Cache] = None):
        self._bucket = bucket_name
        self._s3 = s3_client
        self._expiration = 3600

        if cache is None:
            self._cache = Cache(DummyBackend())
        else:
            self._cache = cache

    def set_file(self, loop_id: str, fileobj) -> bool:
        object_name = loop_id

        try:
            self._s3.upload_fileobj(fileobj, self._bucket, object_name)
        except ClientError:
            return False

        return True

    def remove_file(self, loop_id: str) -> bool:
        pass

    def get_file(self, loop_id: str) -> Optional[str]:
        # try to get the url from the cache
        # to reduce network calls to aws
        # probably not actually needed tho
        file_url = self._cache.fetch(loop_id)

        if file_url is None:
            new_file = self._get_file_from_s3(loop_id, self._expiration)
            if new_file is not None:
                self._cache.save(loop_id, new_file, self._expiration)
                file_url = new_file

        return file_url

    def _get_file_from_s3(self, loop_id: str, expiration) -> Optional[str]:
        params = {"Bucket": self._bucket, "Key": loop_id}

        # ensure that the object exists
        try:
            self._s3.head_object(Bucket=self._bucket, Key=loop_id)
        except ClientError:
            return None

        try:
            response = self._s3.generate_presigned_url("get_object",
                                                       Params=params,
                                                       ExpiresIn=expiration)
        except ClientError:
            return None

        return response

    def file_exists(self, loop_id: str) -> bool:
        loop = self.get_file(loop_id)
        return loop is not None
