# redis://max:nR91D0mt2k@192.168.0.104:6380/0
import redis
from uuid import uuid4
from datetime import datetime, timedelta


r = redis.Redis(host='192.168.0.104', port=6380, db=0, username='admin', password='nR91D0mt2k')


# Проверка подключения
try:
    # Попытка выполнить команду PING
    response = r.ping()
    if response:
        print("Подключение к Redis успешно!")
    else:
        print("Не удалось подключиться к Redis.")
except Exception as e:
    print(f"Произошла ошибка: {e}")

print(
    datetime.timestamp(datetime.now()),
    '\n',
    datetime.timestamp(datetime.now()+timedelta(minutes=15))
)

user_data = {'login': 'max',
             'role': 'admin',
             'b_datetime': datetime.timestamp(datetime.now()),
             'e_datetime':  datetime.timestamp(datetime.now()+timedelta(minutes=15))}


uuid = str(uuid4())
print(uuid)
r.hset(uuid, mapping=user_data)
print(r.hgetall(uuid))
