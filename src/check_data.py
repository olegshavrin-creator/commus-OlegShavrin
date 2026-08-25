from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# Пути к данным
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASE_FILE = PROJECT_ROOT / "data" / "base" / "komus_base38.parquet"
DYNAMIC_FILE = PROJECT_ROOT / "data" / "features" / "komus_base38_dynamic9.parquet"


# ------------------------------------------------------------
# Загрузка
# ------------------------------------------------------------

print("=" * 70)
print("ПРОВЕРКА ВХОДНЫХ ДАННЫХ")
print("=" * 70)

print(f"\nBASE:")
print(BASE_FILE)

print(f"\nDYNAMIC:")
print(DYNAMIC_FILE)


if not BASE_FILE.exists():
    raise FileNotFoundError(f"Не найден файл:\n{BASE_FILE}")

if not DYNAMIC_FILE.exists():
    raise FileNotFoundError(f"Не найден файл:\n{DYNAMIC_FILE}")


base = pd.read_parquet(BASE_FILE)
dynamic = pd.read_parquet(DYNAMIC_FILE)


# ------------------------------------------------------------
# Общая информация
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("BASE COMPACT")
print("=" * 70)

print("Размер:", base.shape)
print("Столбцов:", len(base.columns))

print("\nПервые столбцы:")
print(base.columns.tolist())


print("\n" + "=" * 70)
print("BASE + DYNAMIC")
print("=" * 70)

print("Размер:", dynamic.shape)
print("Столбцов:", len(dynamic.columns))

print("\nСтолбцы:")
print(dynamic.columns.tolist())


# ------------------------------------------------------------
# Обязательные поля
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ОБЯЗАТЕЛЬНЫЕ ПОЛЯ")
print("=" * 70)

for name, df in [("BASE", base), ("DYNAMIC", dynamic)]:
    print(f"\n{name}:")
    print("INN:", "INN" in df.columns)
    print("DefMark:", "DefMark" in df.columns)


# ------------------------------------------------------------
# Какие признаки добавились
# ------------------------------------------------------------

base_features = set(base.columns) - {"INN", "DefMark"}
dynamic_features = set(dynamic.columns) - {"INN", "DefMark"}

added_features = sorted(dynamic_features - base_features)
removed_features = sorted(base_features - dynamic_features)

print("\n" + "=" * 70)
print("СРАВНЕНИЕ ПРИЗНАКОВ")
print("=" * 70)

print("\nПризнаков BASE:", len(base_features))
print("Признаков DYNAMIC:", len(dynamic_features))

print("\nДобавленные признаки:")
for feature in added_features:
    print("  +", feature)

print("\nПризнаки, отсутствующие в DYNAMIC:")
for feature in removed_features:
    print("  -", feature)


# ------------------------------------------------------------
# Проверка компаний
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ПРОВЕРКА КОМПАНИЙ")
print("=" * 70)

base_inn = set(base["INN"])
dynamic_inn = set(dynamic["INN"])

print("Компаний BASE:", len(base_inn))
print("Компаний DYNAMIC:", len(dynamic_inn))

print("Общих компаний:", len(base_inn & dynamic_inn))
print("Только в BASE:", len(base_inn - dynamic_inn))
print("Только в DYNAMIC:", len(dynamic_inn - base_inn))


# ------------------------------------------------------------
# Проверка целевой переменной
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("DEFMark")
print("=" * 70)

print("\nBASE:")
print(base["DefMark"].value_counts(dropna=False))

print("\nDYNAMIC:")
print(dynamic["DefMark"].value_counts(dropna=False))


# ------------------------------------------------------------
# NaN
# ------------------------------------------------------------

print("\n" + "=" * 70)
print("ПРОПУСКИ NaN")
print("=" * 70)

print("\nBASE — всего NaN:", int(base.isna().sum().sum()))
print("DYNAMIC — всего NaN:", int(dynamic.isna().sum().sum()))

print("\nNaN в динамических признаках:")

for feature in added_features:
    nan_count = int(dynamic[feature].isna().sum())
    nan_percent = nan_count / len(dynamic) * 100

    print(
        f"  {feature:<35} "
        f"{nan_count:>8} "
        f"({nan_percent:>6.2f}%)"
    )


print("\n" + "=" * 70)
print("ПРОВЕРКА ЗАВЕРШЕНА")
print("=" * 70)