import logging
import sys
import os
from pythonjsonlogger import jsonlogger

logger = logging.getLogger("")

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')   
formatter_json=jsonlogger.JsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
file_handler = logging.FileHandler('app.log')
json_handler = logging.FileHandler("log.json")

stream_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)
json_handler.setFormatter(formatter_json)

logger.handlers = [json_handler]
logger.propagate = True
logger.setLevel(logging.INFO)
""" 
uvicorn_logger = logging.getLogger("uvicorn.error")
uvicorn_logger.handlers = [stream_handler, file_handler]
uvicorn_logger.setLevel(logging.DEBUG) """
