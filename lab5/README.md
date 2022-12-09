# Лабораторная работа №5: Машины опорных векторов.

В практических примерах ниже показано:

* как классифицировать данные с помощью модели SVM
* как использовать конвейеры для подгонки модели и применения её к новым данным
Точность всех моделей оценивается методом перекрёстной проверки по 5 блокам.

## Данные

1.   `fixed_acidity` – постоянная кислотность;
2.   `volatile_acidity` – переменная кислотность;
3.   `citric_acid` – содержание лимонной кислоты;
4.   `residual_sugar` - остаточный сахар;
5.   `chlorides` – содержание хлоридов;
6.   `free_sulfur_dioxide` – содержание диоксида серы в свободном виде;
7.   `total_sulfur_dioxide` – общее содержание диоксида серы;
8.   `density` – плотность;
9.   `pH` – кислотность;
10.  `sulphates` – содержание сульфатов;
11.  `alcohol` – содержание алкоголя;
12.  `quality` – балльная оценка качества вина, от 0 до 10;
13.  `Y` – целевая переменная: 1 = высокое качество (quality > 5), 0 = низкое (quality <= 5).
Данные: winequality-white_for_lab. Источник: https://raw.githubusercontent.com/ania607/ML/main/data/winequality-white_for_lab.csv

# Загрузка данных

Загружаем данные. Откладываем 15% наблюдений для прогноза.

# Преобразование исходных данных и построение моделей
## Стандартизация и переход к главным компонентам

В качестве альтернативных моделей рассмотрим SVM с различными вариантами ядер и логистическую регрессию. Причём предварительно преобразуем пространство исходных показателей с помощью метода главных компонент.
* Доли объяснённой дисперсии по компонентам в PLS:
* [0.281 0.131 0.114 0.091 0.081 0.078 0.064 0.06  0.047 0.029 0.024 0.002] 
* Общая сумма долей: 1.0
* Таким образом, первые две главные компоненты объясняют 41.2% разброса 12 объясняющих переменных.
## Модель логистической регрессии с перекрёстной проверкой
Acc с перекрёстной проверкой  для модели sc_pca_logit : 0.689
## SVM с перекрёстной проверкой

Построим несколько вариантов модели SVM с различными ядерными функциями.
Acc с перекрёстной проверкой  для модели sc_pca_svc : 1.0
# Метод kNN
Реализуем метод k-ближайших соседей с преобразованием PCA.

В ходе обучения модели я менял такие параметры как: n_splits и n_components в PCA (дало прибавку к точности с 0.689 до 0.898)

Acc с перекрёстной проверкой  для модели sc_pca_knn : 0.898

# Прогноз на отложенные наблюдения по лучшей модели

Ещё раз посмотрим на точность построенных моделей. 
![image](https://user-images.githubusercontent.com/91901972/206786063-935fd6b9-021c-48ef-be38-6aada9e7f993.png)

Все модели показывают хорошую точность по показателю  𝐴𝑐𝑐 , при этом самой точной оказывается модель PCA + SVC. Сделаем прогноз на отложенные наблюдения.
![image](https://user-images.githubusercontent.com/91901972/206786265-7833d48b-1cf1-4c93-aa84-2679db6a3f40.png)