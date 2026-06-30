import sys
from src.exception import CustomException

try:
    a = 10 / 0
except Exception as e:
    raise CustomException(e, sys)