"""
Создание и сохранение единого train/test разделения.

Разделение создаётся один раз и затем используется
для всех экспериментов проекта.
"""

from pathlib import Path

import pandas as pd
from sklearn.model_selection import train_test_split


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

EXPERIMENTS_DIR = PROJECT_ROOT / "experiments"

TRAIN_FILE = EXPERIMENTS_DIR / "train_indices.csv"
TEST_FILE = EXPERIMENTS_DIR / "test_indices.csv"


# ============================================================
# Настройки
# ============================================================

TEST_SIZE = 0.20
RANDOM_STATE = 42


# ============================================================
# Создание split
# ============================================================

def create_split():
    print("=" * 70)
    print("СОЗДАНИЕ TRAIN / TEST")
    print("=" * 70)

    df = pd.read_parquet(BASE_FILE)

    print(f"\nВсего строк: {len(df):,}")

    # Индексы исходного датасета
    indices = df.index

    train_idx, test_idx = train_test_split(
        indices,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=df["DefMark"],
    )

    # Сохраняем
    EXPERIMENTS_DIR.mkdir(parents=True, exist_ok=True)

    pd.Series(train_idx, name="index").to_csv(
        TRAIN_FILE,
        index=False,
    )

    pd.Series(test_idx, name="index").to_csv(
        TEST_FILE,
        index=False,
    )

    print("\nРезультат:")
    print(f"TRAIN: {len(train_idx):,}")
    print(f"TEST : {len(test_idx):,}")

    print("\nФайлы:")
    print(TRAIN_FILE)
    print(TEST_FILE)

    # Проверки
    assert len(set(train_idx) & set(test_idx)) == 0
    assert len(train_idx) + len(test_idx) == len(df)

    print("\nПересечение TRAIN / TEST: 0")
    print("Все строки распределены.")
    print("\nГотово.")


if __name__ == "__main__":
    create_split()