import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.stats.proportion import proportions_ztest

def perform_hypothesis_test(data, age_threshold, work_days_threshold):
    # Создание выборок для более старых и более молодых сотрудников
    older_employees = data[data['Возраст'] > age_threshold]
    younger_employees = data[data['Возраст'] <= age_threshold]

    # Получение количества сотрудников, пропустивших более work_days_threshold дней
    older_absent_count = len(older_employees[older_employees['Количество больничных дней'] > work_days_threshold])
    younger_absent_count = len(younger_employees[younger_employees['Количество больничных дней'] > work_days_threshold])

    # Получение общего количества сотрудников в каждой группе
    total_older = len(older_employees)
    total_younger = len(younger_employees)

    # Выполнение z-теста пропорций
    count = np.array([older_absent_count, younger_absent_count])
    nobs = np.array([total_older, total_younger])
    stat, p_value = proportions_ztest(count, nobs, alternative='two-sided')

    older_proportion = older_absent_count / total_older
    younger_proportion = younger_absent_count / total_younger

    return older_proportion, younger_proportion, stat, p_value

def plot_age_distribution(data, age_threshold, work_days_threshold):
    age_counts_younger = data[data['Возраст'] <= age_threshold]['Количество больничных дней']
    age_counts_older = data[data['Возраст'] > age_threshold]['Количество больничных дней']

    age_counts_younger = age_counts_younger[age_counts_younger > work_days_threshold]
    age_counts_older = age_counts_older[age_counts_older > work_days_threshold]

    unique_counts_younger, counts_younger = np.unique(age_counts_younger, return_counts=True)
    unique_counts_older, counts_older = np.unique(age_counts_older, return_counts=True)

    if len(unique_counts_younger) == 0 or len(unique_counts_older) == 0:
        st.write("***Измените данные, график не может быть визуализирован.***")
    else:
        plt.plot(unique_counts_younger, counts_younger, color='blue', label='Младше {} лет'.format(age_threshold),
                 marker='o', linestyle='-', linewidth=2)
        plt.plot(unique_counts_older, counts_older, color='red', label='Старше {} лет'.format(age_threshold),
                 marker='s', linestyle='--', linewidth=2)

        plt.xlabel('Количество пропущенных дней')
        plt.ylabel('Количество значений')
        plt.title('Распределение количества пропущенных дней между возрастными группами')
        plt.legend()

        plt.grid(True, linestyle='--', alpha=0.5)

        plt.xlim(work_days_threshold + 1, max(unique_counts_younger.max(), unique_counts_older.max()) + 1)
        plt.ylim(0, max(counts_younger.max(), counts_older.max()) + 1)

        for x, y in zip(unique_counts_younger, counts_younger):
            plt.text(x, y + 0.3, str(y), ha='center', va='bottom', color='blue')
        for x, y in zip(unique_counts_older, counts_older):
            plt.text(x, y + 0.3, str(y), ha='center', va='bottom', color='red')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()


def plot_age_gender_distribution(data, age_threshold, work_days_threshold, gender):
    age_counts_younger = data[(data['Возраст'] <= age_threshold) & (data['Пол'] == gender)][
        'Количество больничных дней']
    age_counts_older = data[(data['Возраст'] > age_threshold) & (data['Пол'] == gender)]['Количество больничных дней']

    age_counts_younger = age_counts_younger[age_counts_younger > work_days_threshold]
    age_counts_older = age_counts_older[age_counts_older > work_days_threshold]

    unique_counts_younger, counts_younger = np.unique(age_counts_younger, return_counts=True)
    unique_counts_older, counts_older = np.unique(age_counts_older, return_counts=True)

    try:
        plt.plot(unique_counts_younger, counts_younger, color='blue', label=f'Младше {age_threshold} лет',
                 marker='o', linestyle='-', linewidth=2)
        plt.plot(unique_counts_older, counts_older, color='red', label=f'Старше {age_threshold} лет',
                 marker='s', linestyle='--', linewidth=2)

        plt.xlabel('Количество пропущенных дней')
        plt.ylabel('Количество значений')
        plt.title(f'Распределение количества пропущенных дней между возрастными группами ({gender})')
        plt.legend()

        plt.grid(True, linestyle='--', alpha=0.5)

        plt.xlim(work_days_threshold + 1, max(unique_counts_younger.max(), unique_counts_older.max()) + 1)
        plt.ylim(0, max(counts_younger.max(), counts_older.max()) + 1)

        for x, y in zip(unique_counts_younger, counts_younger):
            plt.text(x, y + 0.3, str(y), ha='center', va='bottom', color='blue')
        for x, y in zip(unique_counts_older, counts_older):
            plt.text(x, y + 0.3, str(y), ha='center', va='bottom', color='red')
        st.set_option('deprecation.showPyplotGlobalUse', False)
        st.pyplot()

    except ValueError:
        st.write('***Невозможно визуализировать график. Пожалуйста, измените данные.***')


def update_results(data, age_threshold, work_days_threshold,gender,significance_level):
    # Выполнение и отображение результатов гипотезного тестирования
    older_proportion, younger_proportion, stat, p_value = perform_hypothesis_test(data, age_threshold,
                                                                                   work_days_threshold)
    st.write("**Задаём гипотезы:**")
    # Нулевая гипотеза
    st.write(f"**H0:** Пропорция работников старше {age_threshold} лет, пропустивших более {work_days_threshold} рабочих дней по болезни, не значимо отличается от пропорции работников младше {age_threshold} лет, пропустивших более {work_days_threshold} рабочих дней по болезни.")
    # Альтернативная гипотеза
    st.write(f"**H1:** Пропорция работников старше {age_threshold} лет, пропустивших более {work_days_threshold} рабочих дней по болезни, значимо отличается от пропорции работников младше {age_threshold} лет, пропустивших более {work_days_threshold} рабочих дней по болезни.")
    st.write(f"Доля работников старше {age_threshold} лет, пропустивших более {work_days_threshold} дней: "
             f"{older_proportion:.4f}")
    st.write(f"Доля работников младше {age_threshold} лет, пропустивших более {work_days_threshold} дней: "
             f"{younger_proportion:.4f}")
    st.write("**Z-тест пропорций:**")
    st.write(f"Статистика = {stat:.4f}")
    st.write(f"p-value = {p_value:.4f}")
    st.write(f"Уровень значимости = {significance_level}")
    # Визуализация распределения
    plot_age_distribution(data,age_threshold, work_days_threshold)
    plot_age_gender_distribution(data, age_threshold, work_days_threshold, gender)

    if p_value < 0.05:
        st.write(f'**Вывод:** Гипотеза о различии больничных дней у работников старше {age_threshold} лет и младше {age_threshold} лет подтверждается.')
    else:
        st.write(f'**Вывод:** Нет статистически значимого различия в больничных днях между работниками старше {age_threshold} лет и младше {age_threshold} лет.')


def main():
    st.title('Анализ пропущенных дней по болезни')

    # Загрузка данных
    st.sidebar.title('Загрузка данных')
    file = st.sidebar.file_uploader('Выберите файл CSV', type=['csv'])
    if file is not None:
        data = pd.read_csv(file)
        st.sidebar.success('Файл успешно загружен.')
    else:
        st.sidebar.warning('Пожалуйста, загрузите файл CSV.')

    if file is not None:
        # Отображение общей информации о данных
        st.subheader('Общая информация о данных')
        st.dataframe(data.head())

        # Установка значений порогов по умолчанию как средних значений
        age_threshold_default = int(data['Возраст'].mean())
        work_days_threshold_default = int(data['Количество больничных дней'].mean())

        # Ввод пользовательских параметров
        st.sidebar.title('Настройка параметров')
        age_threshold = st.sidebar.slider('Выберите пороговый возраст', min_value=int(data['Возраст'].min()),
                                          max_value=int(data['Возраст'].max()), value=age_threshold_default, step=1)
        work_days_threshold = st.sidebar.slider('Выберите пороговое количество пропущенных дней',
                                                min_value=int(data['Количество больничных дней'].min()),
                                                max_value=int(data['Количество больничных дней'].max()),
                                                value=work_days_threshold_default, step=1)

        gender = st.sidebar.selectbox('Выберите пол', ('М', 'Ж'))
        significance_level = 0.05

        # Обновление результатов при изменении параметров
        update_results(data, age_threshold, work_days_threshold, gender, significance_level)


if __name__ == '__main__':
    main()
