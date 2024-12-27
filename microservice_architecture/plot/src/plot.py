import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import time

# Путь к логам и результату
log_file = './logs/metric_log.csv'
output_file = './logs/error_distribution.png'

while True:
    try:
        # Проверка наличия файл логов
        if os.path.exists(log_file):
            # Загружаем файл
            df = pd.read_csv(log_file)

            # гистограмма абсолютных ошибок
            plt.figure(figsize=(10, 8))
            sns.histplot(df['absolute_error'], kde=True, bins=10, color='green')
            plt.title('Distribution of Absolute Errors')
            plt.xlabel('Absolute Error')
            plt.ylabel('Count')

            # Сохранение графика
            plt.savefig(output_file)

        else:
            print("Файл metric_log.csv не найден.")

        # Задержка перед следующим обновлением
        time.sleep(5)
    except Exception as e:
        print(f"Ошибка при обработке: {e}")
        time.sleep(5)