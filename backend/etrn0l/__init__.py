from flask import Flask
from mongoengine import connect  # type: ignore
from .controller import AdminController
from .service.mongo import MongoFlashLoopService
from .ext import CustomJSONEncoder

APP = Flask(__name__)
APP.json_encoder = CustomJSONEncoder

flash_loop_service = MongoFlashLoopService("etrn0l")
AdminController(flash_loop_service).register(APP)

