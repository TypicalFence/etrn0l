from flask import Flask
import boto3  # type: ignore
from kyasshu import Cache, MemoryBackend  # type: ignore
from .controller import AdminController, PublicApiController
from .service.mongo import MongoFlashLoopService
from .service.aws import S3FlashFileService
from .ext import CustomJSONEncoder

APP = Flask(__name__)
APP.json_encoder = CustomJSONEncoder


S3_CLIENT = boto3.client("s3", config=boto3.session.Config(signature_version='s3v4'))
S3_BUCKET = "flash-loops"
FLASH_FILE_CACHE = Cache(MemoryBackend())

FLASH_LOOP_SERVICE = MongoFlashLoopService("etrn0l")
FLASH_FILE_SERVICE = S3FlashFileService(S3_CLIENT, S3_BUCKET, FLASH_FILE_CACHE)

AdminController(FLASH_LOOP_SERVICE, FLASH_FILE_SERVICE).register(APP)
PublicApiController(FLASH_LOOP_SERVICE, FLASH_FILE_SERVICE).register(APP)
