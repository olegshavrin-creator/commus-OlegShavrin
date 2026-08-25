"""
Подготовка исходного датасета для KOMUS Model Lab.

Исходный файл:
    Data_final.xlsb

Результат:
    data/base/komus_base38.parquet

В parquet сохраняются:
    - 38 исходных признаков
    - целевая переменная DefMark
"""

from pathlib import Path

import pandas as pd


# ============================================================
# ПУТИ
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SOURCE_FILE = (
    PROJECT_ROOT
    / "data"
    / "source"
    / "Data_final.xlsb"
)

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "base"
    / "komus_base38.parquet"
)


# ============================================================
# 38 исходных признаков
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

TARGET = "DefMark"


# ============================================================
# ПОДГОТОВКА
# ============================================================

def prepare_dataset():

    print("=" * 70)
    print("ПОДГОТОВКА DATASET ДЛЯ KOMUS MODEL LAB")
    print("=" * 70)

    print(f"\nИсходный файл:")
    print(SOURCE_FILE)

    if not SOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Исходный файл не найден:\n{SOURCE_FILE}\n\n"
            "Положите Data_final.xlsb в папку data/source/"
        )

    # --------------------------------------------------------
    # Чтение исходного файла
    # --------------------------------------------------------

    print("\nЧтение исходного датасета...")

    df = pd.read_excel(
        SOURCE_FILE,
        engine="pyxlsb",
    )

    print(f"Размер исходного датасета: {df.shape}")

    # --------------------------------------------------------
    # Проверка колонок
    # --------------------------------------------------------

    required_columns = BASE_FEATURES + [TARGET]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        print("\nОШИБКА: отсутствуют необходимые столбцы:")

        for column in missing_columns:
            print(f"  - {column}")

        raise ValueError(
            "Исходный датасет не соответствует ожидаемой структуре."
        )

    # --------------------------------------------------------
    # Выбор необходимых колонок
    # --------------------------------------------------------

    result = df[required_columns].copy()

    # --------------------------------------------------------
    # Проверки
    # --------------------------------------------------------

    print("\nПроверка:")

    print(f"  Строк: {len(result):,}")
    print(f"  Признаков: {len(BASE_FEATURES)}")
    print(f"  Target: {TARGET}")

    print(
        f"  Дефолтных компаний: "
        f"{int(result[TARGET].sum()):,}"
    )

    print(
        f"  Недефолтных компаний: "
        f"{int((result[TARGET] == 0).sum()):,}"
    )

    # --------------------------------------------------------
    # Сохранение
    # --------------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    result.to_parquet(
        OUTPUT_FILE,
        index=False,
    )

    print("\nГотово!")

    print(f"Сохранено:")
    print(OUTPUT_FILE)

    print(f"\nРазмер parquet: {result.shape}")


# ============================================================
# Точка входа
# ============================================================

if __name__ == "__main__":
    prepare_dataset()