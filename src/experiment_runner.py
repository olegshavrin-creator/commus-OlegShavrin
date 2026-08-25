"""
Запуск одного эксперимента.

Схема:

данные
   ↓
набор признаков
   ↓
TRAIN / TEST
   ↓
модель
   ↓
предсказания
   ↓
AUC / GINI / Recall / F1
"""
from datetime import datetime
from time import perf_counter
from pathlib import Path

import pandas as pd

from src.feature_sets import get_feature_set
from src.models import create_model, get_nan_rule
from src.metrics import calculate_metrics, print_metrics


# ============================================================
# Пути
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASE_FILE = (
    PROJECT_ROOT
    / "data"
    / "base"
    / "komus_base38.parquet"
)

DYNAMIC_FILE = (
    PROJECT_ROOT
    / "data"
    / "features"
    / "komus_base38_dynamic9.parquet"
)

TRAIN_FILE = (
    PROJECT_ROOT
    / "experiments"
    / "train_indices.csv"
)

TEST_FILE = (
    PROJECT_ROOT
    / "experiments"
    / "test_indices.csv"
)


# ============================================================
# Загрузка данных
# ============================================================

def load_data(
    feature_set_name: str,
    selected_features: list[str] | None = None,
):
    """
    Загружает нужный датасет и выбирает признаки.
    """

    if feature_set_name == "BASE COMPACT":
        data_file = BASE_FILE
    else:
        data_file = DYNAMIC_FILE

    df = pd.read_parquet(data_file)

    available_features = get_feature_set(feature_set_name)

    if selected_features is None:
        features = available_features
    else:
        unknown_features = sorted(
            set(selected_features) - set(available_features)
        )

        if unknown_features:
            unknown_text = ", ".join(unknown_features)
            raise ValueError(
                "Выбраны признаки, которых нет в текущем наборе: "
                f"{unknown_text}"
            )

        if not selected_features:
            raise ValueError(
                "Нужно выбрать хотя бы один признак для эксперимента."
            )

        features = selected_features

    X = df[features]
    y = df["DefMark"]

    return df, X, y


# ============================================================
# Загрузка TRAIN / TEST
# ============================================================

def load_split():
    """
    Загружает зафиксированные индексы TRAIN и TEST.
    """

    train_idx = pd.read_csv(TRAIN_FILE)["index"].to_numpy()
    test_idx = pd.read_csv(TEST_FILE)["index"].to_numpy()

    return train_idx, test_idx


# ============================================================
# Запуск эксперимента
# ============================================================

def run_experiment(
    model_name: str,
    feature_set_name: str,
    selected_features: list[str] | None = None,
):
    """
    Запускает один эксперимент.
    """

    start_time = datetime.now()
    start_counter = perf_counter()

    print("\n" + "=" * 70)
    print("ЭКСПЕРИМЕНТ")
    print("=" * 70)

    print(f"\nМодель: {model_name}")
    print(f"Набор признаков: {feature_set_name}")

    # --------------------------------------------------------
    # Данные
    # --------------------------------------------------------

    df, X, y = load_data(
        feature_set_name,
        selected_features=selected_features,
    )

    features = X.columns.tolist()

    print(f"Количество признаков: {len(features)}")

    # --------------------------------------------------------
    # TRAIN / TEST
    # --------------------------------------------------------

    train_idx, test_idx = load_split()

    X_train = X.iloc[train_idx]
    X_test = X.iloc[test_idx]

    y_train = y.iloc[train_idx]
    y_test = y.iloc[test_idx]

    print(f"\nTRAIN: {len(X_train):,}")
    print(f"TEST : {len(X_test):,}")

    # --------------------------------------------------------
    # NaN
    # --------------------------------------------------------

    print(
        f"\nОбработка NaN: "
        f"{get_nan_rule(model_name)}"
    )

    # --------------------------------------------------------
    # Модель
    # --------------------------------------------------------

    model = create_model(model_name)

    print("\nОбучение модели...")

    model.fit(X_train, y_train)

    print("Обучение завершено.")

    # --------------------------------------------------------
    # Предсказания
    # --------------------------------------------------------

    y_proba = model.predict_proba(X_test)[:, 1]

    # --------------------------------------------------------
    # Метрики
    # --------------------------------------------------------

    metrics = calculate_metrics(
        y_test,
        y_proba,
    )

    print_metrics(metrics)

    # --------------------------------------------------------
    # Время выполнения
    # --------------------------------------------------------

    end_time = datetime.now()
    elapsed_seconds = perf_counter() - start_counter

    print(f"\nВремя выполнения: {elapsed_seconds:.2f} сек.")

    # --------------------------------------------------------
    # Сохранение эксперимента в историю
    # --------------------------------------------------------

    LOG_FILE = PROJECT_ROOT / "experiments" / "experiment_log.csv"

    result = {
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "elapsed_seconds": round(elapsed_seconds, 2),
        "model": model_name,
        "feature_set": (
            feature_set_name
            if selected_features is None
            else f"{feature_set_name} CUSTOM"
        ),
        "n_features": len(features),
        "train_size": len(X_train),
        "test_size": len(X_test),
        **metrics,
    }

    # В истории храним только 8 полей,
    # которые использует текущий интерфейс
    history_row = pd.DataFrame([{
        "start_time": result["start_time"],
        "model": result["model"],
        "feature_set": result["feature_set"],
        "GINI": result["GINI"],
        "AUC": result["AUC"],
        "Recall": result["Recall"],
        "F1": result["F1"],
        "elapsed_seconds": result["elapsed_seconds"],
    }])

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    history_row.to_csv(
        LOG_FILE,
        mode="a",
        header=False,
        index=False,
        encoding="utf-8-sig",
        lineterminator="\n",
    )

    return result
    


# ============================================================
# Тестовый запуск
# ============================================================

if __name__ == "__main__":

    result = run_experiment(
        model_name="LightGBM",
        feature_set_name="BASE + SPARK",
    )

    print("\nИтоговый результат:")
    print(result)
