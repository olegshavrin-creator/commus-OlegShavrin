"""
Сравнение моделей и наборов признаков.

Запускает серию экспериментов:

LightGBM       × BASE COMPACT
LightGBM       × BASE + SPARK
CatBoost       × BASE COMPACT
CatBoost       × BASE + SPARK
Logistic       × BASE COMPACT
Logistic       × BASE + SPARK

Все эксперименты используют один и тот же TRAIN / TEST.
"""

import pandas as pd

from src.experiment_runner import run_experiment

from datetime import datetime
from time import perf_counter
# ============================================================
# Что сравниваем
# ============================================================

MODELS = [
    "LightGBM",
    "CatBoost",
    "Logistic Regression",
]

FEATURE_SETS = [
    "BASE COMPACT",
    "BASE + SPARK",
]


# ============================================================
# Запуск сравнения
# ============================================================

def run_comparison():

    results = []

    total = len(MODELS) * len(FEATURE_SETS)
    current = 0

    print("\n" + "=" * 70)
    print("СРАВНЕНИЕ МОДЕЛЕЙ И НАБОРОВ ПРИЗНАКОВ")
    print("=" * 70)

    print(f"\nВсего экспериментов: {total}")

    for model_name in MODELS:

        for feature_set_name in FEATURE_SETS:

            current += 1

            print("\n")
            print("#" * 70)
            print(f"ЭКСПЕРИМЕНТ {current} / {total}")
            print("#" * 70)

            # Начало эксперимента
            start_time = datetime.now()
            start_counter = perf_counter()

            # Запуск модели
            result = run_experiment(
                model_name=model_name,
                feature_set_name=feature_set_name,
            )

            # Конец эксперимента
            end_time = datetime.now()
            elapsed_seconds = perf_counter() - start_counter

            # Добавляем информацию о времени
            result["start_time"] = start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            result["end_time"] = end_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            )
            result["elapsed_seconds"] = round(
                elapsed_seconds, 2
            )

            # Размеры TRAIN / TEST
            result["train_size"] = 289614
            result["test_size"] = 72404

            print(
                f"\nВремя эксперимента: "
                f"{elapsed_seconds:.2f} сек."
            )

            results.append(result)

    return pd.DataFrame(results)

# ============================================================
# Красивый вывод
# ============================================================

def print_comparison_table(results_df):

    print("\n\n")
    print("=" * 90)
    print("ИТОГОВОЕ СРАВНЕНИЕ")
    print("=" * 90)

    table = results_df.copy()

    for column in ["AUC", "GINI", "Recall", "F1"]:
        table[column] = table[column].map(
            lambda x: f"{x:.6f}"
        )

    print(
        table.to_string(index=False)
    )

    print("=" * 90)


# ============================================================
# Сохранение
# ============================================================

def save_results(results_df):

    comparison_file = "experiments/model_comparison.csv"
    log_file = "experiments/experiment_log.csv"

    # ========================================================
    # Краткая таблица результатов
    # ========================================================

    comparison_columns = [
        "model",
        "feature_set",
        "n_features",
        "AUC",
        "GINI",
        "Recall",
        "F1",
    ]

    results_df[comparison_columns].to_csv(
        comparison_file,
        index=False,
    )

    # ========================================================
    # Полный лог экспериментов
    # ========================================================

    log_columns = [
        "start_time",
        "end_time",
        "elapsed_seconds",
        "model",
        "feature_set",
        "n_features",
        "train_size",
        "test_size",
        "AUC",
        "GINI",
        "Recall",
        "F1",
    ]

    results_df[log_columns].to_csv(
        log_file,
        index=False,
    )

    print("\nРезультаты сохранены:")
    print(comparison_file)

    print("\nЛог экспериментов:")
    print(log_file)

# ============================================================
# Запуск
# ============================================================

if __name__ == "__main__":

    results = run_comparison()

    print_comparison_table(results)

    save_results(results)