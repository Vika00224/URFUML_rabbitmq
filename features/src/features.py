import pika
import numpy as np
import json
from sklearn.datasets import load_diabetes
import time
from datetime import datetime

# Загружаем датасет о диабете
X, y = load_diabetes(return_X_y=True)

# Создаём бесконечный цикл для отправки сообщений в очередь
while True:
    try:
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

        # Формируем сообщение для y_true с уникальным идентификатором
        message_y_true = {
            'id': message_id,
            'body': y[random_row].tolist()  # Преобразуем в список для сериализации
        }
        
        # Публикуем сообщение в очередь y_true
        channel.basic_publish(exchange='',
                              routing_key='y_true',
                              body=json.dumps(message_y_true))
        print('Сообщение с правильным ответом отправлено в очередь')

        # Формируем сообщение для features с тем же уникальным идентификатором
        message_features = {
            'id': message_id,
            'body': list(X[random_row])  # Преобразуем в список для сериализации
        }
        
        # Публикуем сообщение в очередь features
        channel.basic_publish(exchange='',
                              routing_key='features',
                              body=json.dumps(message_features))
        print('Сообщение с вектором признаков отправлено в очередь')

        # Закрываем подключение
        connection.close()

        # Задержка перед следующей итерацией (например, 1 секунда)
        time.sleep(1)

    except Exception as e:
        print(f'Не удалось подключиться к очереди: {e}')
