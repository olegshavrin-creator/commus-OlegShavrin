"""
Модели для экспериментов.

Здесь:
1. хранятся параметры моделей;
2. создаются выбранные модели;
3. определяются правила обработки NaN;
4. все доступные модели зарегистрированы в MODEL_REGISTRY.

Для добавления новой модели достаточно:
- определить её параметры;
- создать функцию-фабрику;
- добавить модель в MODEL_REGISTRY.
"""

from typing import Any, Callable

from catboost import CatBoostClassifier
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


# ============================================================
# Параметры LightGBM
# ============================================================

LIGHTGBM_PARAMS = {
    "learning_rate": 0.05,
    "max_depth": 10,
    "metric": "auc",
    "n_estimators": 300,
    "n_jobs": -1,
    "num_leaves": 40,
    "objective": "binary",
    "random_state": 42,
    "reg_alpha": 0.5,
    "reg_lambda": 0.1,
    "verbose": -1,
}


# ============================================================
# Параметры CatBoost
# ============================================================

CATBOOST_PARAMS = {
    "iterations": 300,
    "learning_rate": 0.05,
    "depth": 6,
    "random_seed": 42,
    "verbose": False,
}


# ============================================================
# Параметры Logistic Regression
# ============================================================

LOGISTIC_PARAMS = {
    "max_iter": 1000,
    "random_state": 42,
}


# ============================================================
# Параметры XGBoost
# ============================================================

XGBOOST_PARAMS = {
    "n_estimators": 300,
    "learning_rate": 0.05,
    "max_depth": 6,
    "subsample": 0.8,
    "colsample_bytree": 0.8,
    "objective": "binary:logistic",
    "eval_metric": "auc",
    "random_state": 42,
    "n_jobs": -1,
}


# ============================================================
# Параметры Random Forest
# ============================================================

RANDOM_FOREST_PARAMS = {
    "n_estimators": 300,
    "max_depth": None,
    "min_samples_split": 2,
    "min_samples_leaf": 1,
    "random_state": 42,
    "n_jobs": -1,
    "class_weight": "balanced",
}


# ============================================================
# Фабрики моделей
# ============================================================

def create_lightgbm() -> Any:
    return LGBMClassifier(**LIGHTGBM_PARAMS)


def create_catboost() -> Any:
    return CatBoostClassifier(**CATBOOST_PARAMS)


def create_logistic_regression() -> Any:
    return Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "scaler",
            StandardScaler(),
        ),
        (
            "model",
            LogisticRegression(**LOGISTIC_PARAMS),
        ),
    ])


def create_xgboost() -> Any:
    return XGBClassifier(**XGBOOST_PARAMS)


def create_random_forest() -> Any:
    return Pipeline([
        (
            "imputer",
            SimpleImputer(strategy="median"),
        ),
        (
            "model",
            RandomForestClassifier(**RANDOM_FOREST_PARAMS),
        ),
    ])


# ============================================================
# Реестр моделей
# ============================================================

MODEL_REGISTRY: dict[str, dict[str, Any]] = {

    "LightGBM": {
        "factory": create_lightgbm,
        "nan_rule": "оставляем NaN",
    },

    "CatBoost": {
        "factory": create_catboost,
        "nan_rule": "оставляем NaN",
    },

    "Logistic Regression": {
        "factory": create_logistic_regression,
        "nan_rule": "заполняем медианой",
    },

    "XGBoost": {
        "factory": create_xgboost,
        "nan_rule": "оставляем NaN",
    },

    "Random Forest": {
        "factory": create_random_forest,
        "nan_rule": "заполняем медианой",
    },
}


# ============================================================
# Названия доступных моделей
# ============================================================

MODEL_NAMES = list(MODEL_REGISTRY.keys())


# ============================================================
# Создание выбранной модели
# ============================================================

def create_model(name: str) -> Any:
    """
    Создаёт модель по названию.
    """

    if name not in MODEL_REGISTRY:
        raise ValueError(
            f"Неизвестная модель: {name}. "
            f"Доступные модели: {', '.join(MODEL_NAMES)}"
        )

    factory: Callable[[], Any] = MODEL_REGISTRY[name]["factory"]

    return factory()


# ============================================================
# Правило обработки NaN
# ============================================================

def get_nan_rule(model_name: str) -> str:
    """
    Возвращает описание обработки NaN
    для выбранной модели.
    """

    if model_name not in MODEL_REGISTRY:
        raise ValueError(
            f"Неизвестная модель: {model_name}"
        )

    return MODEL_REGISTRY[model_name]["nan_rule"]