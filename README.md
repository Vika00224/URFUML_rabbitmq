# URFUML_RabbitMQ
## Бизнес-применение машинного обучения. Домашнее задание №1 (HW)
В рамках задания реализовано:
1. Сервисы работают в режиме бесконечного цикла и обмениваются между собой сообщениями через AMQP-протокол.
2. Временная задержка между отправкой признаков и истинных ответов в сервисе features.
3. Использование уникальных идентификаторов в сообщениях.
4. Логирование предсказаний, ответов и абсолютных ошибок в файл metric_log.csv.
5. Построение гистограммы абсолютных ошибок на основе данных из metric_log.csv.
