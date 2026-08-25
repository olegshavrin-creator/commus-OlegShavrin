"""
Метрики качества моделей.

Используем:
- AUC — площадь под ROC-кривой;
- GINI — основная метрика кредитного скоринга;
- Recall — какую долю дефолтов модель нашла;
- F1 — баланс точности и полноты.
"""

import numpy as np

from sklearn.metrics import (
    roc_auc_score,
    recall_score,
    f1_score,
)


def calculate_metrics(y_true, y_proba, threshold=0.5):
    """
    Рассчитывает основные метрики модели.

    y_true:
        настоящие значения DefMark.

    y_proba:
        вероятность класса 1 (дефолта).

    threshold:
        порог, выше которого считаем компанию дефолтной.
    """

    # Приводим входные данные к NumPy-массивам.
    # Поэтому функция работает и со списками, и с pandas Series.
    y_true = np.asarray(y_true)
    y_proba = np.asarray(y_proba)

    # AUC
    auc = roc_auc_score(y_true, y_proba)

    # GINI
    gini = 2 * auc - 1

    # Перевод вероятностей в 0/1
    y_pred = (y_proba >= threshold).astype(int)

    # Recall
    recall = recall_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    # F1
    f1 = f1_score(
        y_true,
        y_pred,
        zero_division=0,
    )

    return {
        "AUC": auc,
        "GINI": gini,
        "Recall": recall,
        "F1": f1,
    }


def print_metrics(metrics):
    """
    Красиво выводит результаты эксперимента.
    """

    print("\n" + "=" * 50)
    print("РЕЗУЛЬТАТ МОДЕЛИ")
    print("=" * 50)

    print(f"AUC    : {metrics['AUC']:.6f}")
    print(f"GINI   : {metrics['GINI']:.6f}")
    print(f"Recall : {metrics['Recall']:.6f}")
    print(f"F1     : {metrics['F1']:.6f}")

    print("=" * 50)