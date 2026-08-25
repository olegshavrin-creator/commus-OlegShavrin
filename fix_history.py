from pathlib import Path
import pandas as pd

LOG_FILE = Path("experiments/experiment_log.csv")

df = pd.read_csv(LOG_FILE)

print("Было:")
print(df.columns.tolist())
print()
print(df)

# Оставляем только нужные для интерфейса поля
history = df[
    [
        "start_time",
        "model",
        "feature_set",
        "GINI",
        "AUC",
        "Recall",
        "F1",
        "elapsed_seconds",
    ]
].copy()

# Правильный порядок
history = history[
    [
        "start_time",
        "model",
        "feature_set",
        "GINI",
        "AUC",
        "Recall",
        "F1",
        "elapsed_seconds",
    ]
]

history.to_csv(
    LOG_FILE,
    index=False,
    encoding="utf-8-sig",
)

print()
print("После:")
print(history.columns.tolist())
print()
print(history)
print()
print(f"Сохранено: {LOG_FILE}")