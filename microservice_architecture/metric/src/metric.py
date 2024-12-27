import os
import pandas as pd
import pika
import json

# Путь к файлу логов
log_path = './logs/metric_log.csv'

# Заголовки для файла
headers = ['id', 'y_true', 'y_pred', 'absolute_error']

if not os.path.exists(log_path):
    pd.DataFrame(columns=headers).to_csv(log_path, index=False)

# Проверка и добавление заголовков
else:
    with open(log_path, 'r') as file:
        first_line = file.readline().strip()
    if first_line != ",".join(headers):  # Если заголовков нет
        pd.DataFrame(columns=headers).to_csv(log_path, index=False)

#  для временного хранения данных
true_dict = {}
pred_dict = {}


# записывает в файл
def write_log():
    # Проверяем, есть ли файл и содержит ли он заголовки
    if not os.path.exists(log_path):
        pd.DataFrame(columns=headers).to_csv(log_path, index=False)
    else:
        with open(log_path, 'r') as file:
            first_line = file.readline().strip()
        if first_line != ','.join(headers):  # Если заголовков нет
            pd.DataFrame(columns=headers).to_csv(log_path, index=False)

    # Добавляем строки с данными
    for message_id in set(true_dict) & set(pred_dict):
        y_true = true_dict.pop(message_id)
        y_pred = pred_dict.pop(message_id)
        error = abs(y_true - y_pred)  # расчет абсолютной ошибки
        row = {'id': message_id, 'y_true': y_true, 'y_pred': y_pred, 'absolute_error': error}
        pd.DataFrame([row]).to_csv(log_path, mode='a', header=False, index=False)


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()

    # объявляем очереди y_true и y_pred
    channel.queue_declare(queue='y_true')
    channel.queue_declare(queue='y_pred')


    # Обработка сообщение y_true
    def callback_y_true(ch, method, properties, body):
        msg = json.loads(body)
        true_dict[msg['id']] = msg['body']
        write_log()


    # Обработка сообщение y_pred.
    def callback_y_pred(ch, method, properties, body):
        msg = json.loads(body)
        pred_dict[msg['id']] = msg['body']
        write_log()


    # получаем сообщения и обрабатываем их
    channel.basic_consume(queue='y_true', on_message_callback=callback_y_true, auto_ack=True)
    channel.basic_consume(queue='y_pred', on_message_callback=callback_y_pred, auto_ack=True)
    print("Ожидание сообщений. Нажмите CTRL+C для выхода.")
    channel.start_consuming()

except Exception as e:
    print(f"Ошибка подключения или обработки: {e}")