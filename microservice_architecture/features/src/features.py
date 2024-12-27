import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime

# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
        # Загружаем датасет о диабете
        X, y = load_diabetes(return_X_y=True)
        
        # Формируем случайный индекс строки
        random_row = np.random.randint(0, X.shape[0]-1)
        
        # Генерируем уникальный идентификатор на основе текущего времени (timestamp)
        message_id = int(datetime.now().timestamp())

        # Создаём подключение по адресу rabbitmq:
        connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
        channel = connection.channel()

        # Создаём очередь y_true, если она не существует
        channel.queue_declare(queue='y_true')
        # Создаём очередь features, если она не существует
        channel.queue_declare(queue='features')

        # Формируем сообщение с ID
        message_y_true = {'id': message_id, 'body': y[random_row]}
        message_features = {'id': message_id, 'body': list(X[random_row])}
        
        # Публикуем сообщения в соответствующую очередь
        channel.basic_publish(exchange='', routing_key='y_true', body=json.dumps(message_y_true))
        channel.basic_publish(exchange='', routing_key='features', body=json.dumps(message_features))
        print(f"Сообщение {message_id} отправлено.")

        # Закрываем подключение
        connection.close()

        # Задержка перед следующей итерацией 5 секунд
        time.sleep(5)

    except Exception as e:
        print(f'Не удалось подключиться к очереди: {e}')
        time.sleep(5)