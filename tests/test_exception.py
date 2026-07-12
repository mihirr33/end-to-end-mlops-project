from src.exception import CustomException
import sys

try:
    a = 10 / 0

except Exception as e:
    error = CustomException(e, sys)

    print(error)

print("Exception Test Passed")