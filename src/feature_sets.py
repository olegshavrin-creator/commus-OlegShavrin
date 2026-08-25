"""
Наборы признаков для экспериментов.

Здесь храним только описание наборов.
Никакого обучения моделей здесь нет.
"""

# ============================================================
# Базовые признаки
# ============================================================

BASE_FEATURES = [
    "Q_A1_norm",
    "Q_A4_norm",
    "Q_A5_norm",
    "Q_A6_norm",
    "Q_B3_norm",
    "Q_C1_norm",
    "Q_D4_norm",
    "Q_D6_norm",

    "A1_norm",
    "A2_norm",
    "A3_norm",
    "A4_norm",
    "A5_norm",
    "A6_norm",

    "B1_norm",
    "B2_norm",
    "B3_norm",

    "C1_norm",
    "C2_norm",
    "C3_norm",
    "C4_norm",

    "D1_norm",
    "D2_norm",
    "D3_norm",
    "D4_norm",
    "D5_norm",

    "E1_norm",
    "E2_norm",
    "E3_norm",

    "F1_norm",
    "F2_norm",
    "F3_norm",
    "F4_norm",

    "G1_norm",
    "G2_norm",
    "G3_norm",
    "G4_norm",
    "G5_norm",
]


# ============================================================
# Новые динамические признаки SPARK
# ============================================================

SPARK_DYNAMIC_FEATURES = [
    "spark_revenue_growth_1y",
    "spark_equity_growth_1y",
    "spark_profit_growth_1y",
    "spark_equity_last",
    "spark_profit_margin_last",
    "spark_profit_margin_change_1y",
    "spark_revenue_last",
    "spark_loss_last_year",
    "spark_loss_count_3y",
]


# ============================================================
# Готовые наборы
# ============================================================

FEATURE_SETS = {
    "BASE COMPACT": BASE_FEATURES,

    "BASE + SPARK": BASE_FEATURES + SPARK_DYNAMIC_FEATURES,

    "SPARK ONLY": SPARK_DYNAMIC_FEATURES,
}


# ============================================================
# Проверки
# ============================================================

assert len(BASE_FEATURES) == 38
assert len(SPARK_DYNAMIC_FEATURES) == 9
assert len(FEATURE_SETS["BASE + SPARK"]) == 47


# ============================================================
# Вспомогательная функция
# ============================================================

def get_feature_set(name: str) -> list[str]:
    """
    Возвращает список признаков по названию набора.
    """

    if name not in FEATURE_SETS:
        available = ", ".join(FEATURE_SETS.keys())

        raise ValueError(
            f"Неизвестный набор признаков: {name}\n"
            f"Доступные наборы: {available}"
        )

    return FEATURE_SETS[name].copy()