import pickle
import os
import pika
import json
import numpy as np

# Путь к файлу модели
model_path = os.path.join(os.getcwd(), "myfile.pkl")

# Проверяем, существует ли файл модели
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Файл модели не найден: {model_path}")

# Загружаем модель
with open(model_path, 'rb') as pkl_file:
    regressor = pickle.load(pkl_file)

print("Модель успешно загружена!")

# Подключение к RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # объявляем очереди features и y_pred
    channel.queue_declare(queue='features')
    channel.queue_declare(queue='y_pred')

    # функция обработки данных из очереди
    def callback(ch, method, properties, body):
        try:
            print(f'Получено сообщение: {body}')
            message = json.loads(body)
            if 'body' not in message:
                raise ValueError("Сообщение не содержит ключа 'body'")
            features = np.array(message['body'], dtype=float).reshape(1, -1)
            pred = regressor.predict(features)
            # формируем и публикуем сообщение с тем же id
            channel.basic_publish(exchange='', routing_key='y_pred', body=json.dumps({'id': message['id'], 'body': pred[0]}))
            print(f"Отправлено предсказание: {pred[0]}")
        except Exception as e:
            print(f"Ошибка в обработке сообщения: {e}")

    # Извлекаем сообщение из очереди features
    channel.basic_consume(queue='features', on_message_callback=callback, auto_ack=True)
    print("Ожидание сообщений. Нажмите CTRL+C для выхода.")
    # режим ожидания сообщений
    channel.start_consuming()

except Exception as e:
    print(f"Ошибка подключения или обработки: {e}")