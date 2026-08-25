import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from streamlit import column_config


st.set_page_config(
    page_title="KOMUS Model Lab",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7faff !important;
    }

    header[data-testid="stHeader"] {
        background: transparent !important;
        height: 0 !important;
    }

    footer {
        visibility: hidden;
    }

    .main-header {
        background: linear-gradient(135deg, #0b2d5c 0%, #1261a0 100%);
        padding: 14px 20px;
        border-radius: 12px;
        margin-top: 6px;
        margin-bottom: 10px;
        box-shadow: 0 4px 15px rgba(11, 45, 92, 0.15);
    }

    .main-title {
        margin: 0;
        color: #ffffff !important;
        font-size: 24px;
        font-weight: 700;
    }

    .main-subtitle {
        margin-top: 2px;
        color: #ffffff !important;
        font-size: 13px;
        opacity: 0.9;
    }

    .section-title {
        margin-bottom: 8px;
        color: #0b2d5c !important;
        font-size: 17px;
        font-weight: 700;
    }

    .block-container {
        padding-top: 0.6rem !important;
        padding-bottom: 1.5rem !important;
    }

    div[data-testid="stToolbar"] {
        display: none !important;
    }

    div[data-testid="stHorizontalBlock"] {
        align-items: flex-start;
    }

    [data-testid="stWidgetLabel"] p {
        color: #0b2d5c !important;
        font-size: 14px !important;
        font-weight: 600 !important;
    }

    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border: 1px solid #b9d2e8 !important;
        border-radius: 9px !important;
        color: #0b2d5c !important;
    }

    div[data-baseweb="select"] span {
        color: #0b2d5c !important;
    }

    div[data-baseweb="select"] svg {
        fill: #1261a0 !important;
    }

    div[data-baseweb="popover"] {
        background-color: #0b2d5c !important;
        border: 1px solid #1261a0 !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="popover"] ul {
        background-color: #0b2d5c !important;
    }

    div[data-baseweb="popover"] li {
        background-color: #0b2d5c !important;
        color: #ffffff !important;
    }

    div[data-baseweb="popover"] li:hover,
    div[data-baseweb="popover"] li[aria-selected="true"] {
        background-color: #1261a0 !important;
        color: #ffffff !important;
    }

    div[data-baseweb="popover"] li span {
        color: #ffffff !important;
    }

    .base-info,
    .spark-info {
        border-radius: 10px;
        padding: 12px 14px;
        font-size: 14px;
    }

    .base-info {
        background-color: #d9e9fa !important;
        border: 1px solid #c4dcef;
        color: #17446f !important;
    }

    .spark-info {
        background-color: #e3f1e6 !important;
        border: 1px solid #c3dfc9;
        color: #164d2b !important;
        line-height: 1.45;
    }

    .base-info b {
        color: #123f68 !important;
    }

    .spark-info b {
        color: #0f542b !important;
    }

    .spark-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background-color: #dff0ff;
        color: #1261a0 !important;
        font-size: 12px;
        font-weight: 700;
    }

    .stButton > button {
        width: 100%;
        height: 45px;
        background-color: #1261a0 !important;
        border: 1px solid #1261a0 !important;
        border-radius: 9px !important;
        color: #ffffff !important;
        font-weight: 700;
        box-shadow: 0 3px 8px rgba(18, 97, 160, 0.20);
    }

    .stButton > button:hover {
        background-color: #0b4f88 !important;
        border-color: #0b4f88 !important;
        color: #ffffff !important;
    }

    .stButton > button:active {
        background-color: #083b68 !important;
        color: #ffffff !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px !important;
    }

    .result-box,
    .panel-card {
        background-color: #ffffff !important;
        border: 1px solid #d9e6f2;
        border-radius: 14px;
        box-shadow: 0 3px 12px rgba(11, 45, 92, 0.07);
    }

    .result-box {
        padding: 18px;
        color: #0b2d5c !important;
    }

    .panel-card {
        padding: 18px 18px 16px 18px;
        margin-bottom: 18px;
    }

    .result-box b {
        color: #0b2d5c !important;
    }

    .empty-result {
        min-height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
        color: #0b2d5c !important;
    }

    .empty-icon {
        margin-bottom: 10px;
        color: #1261a0 !important;
        font-size: 42px;
        font-weight: 700;
    }

    .empty-title {
        color: #0b2d5c !important;
        font-size: 22px;
        font-weight: 700;
    }

    .empty-text {
        margin-top: 8px;
        color: #60758a !important;
        line-height: 1.6;
    }

    .metric-card {
        background-color: #ffffff !important;
        border: 1px solid #cfe0ef;
        border-radius: 12px;
        padding: 18px;
        box-shadow: 0 3px 10px rgba(11, 45, 92, 0.08);
        text-align: center;
    }

    .metric-label {
        color: #60758a !important;
        font-size: 13px;
        font-weight: 600;
    }

    .metric-value {
        margin-top: 5px;
        color: #1261a0 !important;
        font-size: 28px;
        font-weight: 700;
    }

    .feature-table-wrapper {
        width: 100%;
        max-height: 260px;
        overflow-y: auto;
        overflow-x: auto;
        border: 1px solid #d7e2ec;
        border-radius: 10px;
        background: #ffffff;
        margin-top: 10px;
    }

    .feature-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
        background: #ffffff !important;
        color: #17324d !important;
        font-size: 14px;
    }

    .feature-table thead th {
        position: sticky;
        top: 0;
        z-index: 2;
        background: #eaf2f8 !important;
    }

    .feature-table th {
        padding: 12px 14px;
        border-bottom: 1px solid #cbd9e5;
        color: #17324d !important;
        font-weight: 700;
        text-align: left;
    }

    .feature-table td {
        padding: 10px 14px;
        border-bottom: 1px solid #e1e8ee;
        background: #ffffff !important;
        color: #17324d !important;
        vertical-align: middle;
    }

    .feature-table th:nth-child(1),
    .feature-table td:nth-child(1) {
        width: 170px;
    }

    .feature-table th:nth-child(2),
    .feature-table td:nth-child(2) {
        width: 220px;
    }

    .feature-table th:nth-child(3),
    .feature-table td:nth-child(3) {
        width: auto;
    }

    .feature-table th:nth-child(4),
    .feature-table td:nth-child(4) {
        width: 120px;
    }

    .feature-table code {
        padding: 3px 6px;
        border-radius: 4px;
        background: #f1f5f8 !important;
        color: #17324d !important;
        font-family: monospace;
        font-size: 13px;
    }

    .feature-badge {
        display: inline-block;
        padding: 4px 8px;
        border-radius: 6px;
        font-size: 11px;
        font-weight: 700;
        white-space: nowrap;
    }

    .badge-used {
        background: #dff3e3 !important;
        color: #18743b !important;
    }

    .badge-weak {
        background: #dff0ff !important;
        color: #1769aa !important;
    }

    .badge-marker {
        background: #ffdede !important;
        color: #b42318 !important;
    }

    .feature-table tr.feature-weak td {
        background: #f2f9ff !important;
    }

    .feature-table tr.feature-marker td {
        background: #fff4f4 !important;
    }

    .feature-table tbody tr:hover td {
        background: #eef6fc !important;
    }

    .catalog-note {
        color: #60758a !important;
        font-size: 13px;
        margin-bottom: 4px;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #cbd9e5 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        background: #ffffff !important;
    }

    div[data-testid="stDataFrame"] * {
        color: #17324d !important;
    }

    div[data-testid="stDataFrame"] [role="columnheader"] {
        background: #eaf2f8 !important;
        color: #17324d !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDataFrame"] [role="gridcell"] {
        background: #ffffff !important;
        border-color: #dbe6f0 !important;
    }

    div[data-testid="stDataFrame"] input,
    div[data-testid="stDataFrame"] textarea {
        color: #17324d !important;
        background: #ffffff !important;
    }

    div[data-testid="stDataEditor"] {
        background: #ffffff !important;
        border: 1px solid #cbd9e5 !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    div[data-testid="stDataEditor"] * {
        color: #17324d !important;
    }

    div[data-testid="stDataEditor"] [role="columnheader"] {
        background: #eaf2f8 !important;
        color: #17324d !important;
        font-weight: 700 !important;
    }

    div[data-testid="stDataEditor"] [role="gridcell"] {
        background: #ffffff !important;
        border-color: #dbe6f0 !important;
    }

    div[data-testid="stDataEditor"] input,
    div[data-testid="stDataEditor"] textarea,
    div[data-testid="stDataEditor"] label,
    div[data-testid="stDataEditor"] span,
    div[data-testid="stDataEditor"] p {
        color: #17324d !important;
        background: transparent !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
FEATURE_REGISTRY_FILE = PROJECT_ROOT / "data" / "feature_registry.csv"
LOG_FILE = PROJECT_ROOT / "experiments" / "experiment_log.csv"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.experiment_runner import run_experiment
from src.feature_sets import get_feature_set


def render_header() -> None:
    st.markdown(
        """
        <div class="main-header">
            <div class="main-title">KOMUS MODEL LAB</div>
            <div class="main-subtitle">
                Витрина запуска экспериментов и анализа признаков
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def build_feature_table_html(registry: pd.DataFrame) -> str:
    rows_html = []

    for _, row in registry.iterrows():
        status = str(row.get("status", ""))
        feature = str(row.get("feature", ""))
        name = str(row.get("display_name", ""))
        source = str(row.get("source", ""))

        if name == "nan":
            name = "—"

        if status == "Используется":
            row_class = "feature-used"
            badge_class = "badge-used"
            badge_text = "ИСПОЛЬЗУЕТСЯ"
        elif status == "Маркер":
            row_class = "feature-marker"
            badge_class = "badge-marker"
            badge_text = "МАРКЕР"
        elif status == "Слабый / избыточный":
            row_class = "feature-weak"
            badge_class = "badge-weak"
            badge_text = "СЛАБЫЙ / ИЗБЫТОЧНЫЙ"
        else:
            row_class = ""
            badge_class = ""
            badge_text = status

        rows_html.append(
            f"""
            <tr class="{row_class}">
                <td><span class="feature-badge {badge_class}">{badge_text}</span></td>
                <td><code>{feature}</code></td>
                <td>{name}</td>
                <td>{source}</td>
            </tr>
            """
        )

    return f"""
    <div class="feature-table-wrapper">
        <table class="feature-table">
            <thead>
                <tr>
                    <th>Статус</th>
                    <th>Техническое имя</th>
                    <th>Русское название</th>
                    <th>Источник</th>
                </tr>
            </thead>
            <tbody>
                {''.join(rows_html)}
            </tbody>
        </table>
    </div>
    """


def load_feature_registry() -> pd.DataFrame:
    if not FEATURE_REGISTRY_FILE.exists():
        return pd.DataFrame()

    return pd.read_csv(
        FEATURE_REGISTRY_FILE,
        encoding="utf-8-sig",
    )


def save_feature_registry_updates(edited_registry: pd.DataFrame) -> None:
    registry = load_feature_registry()

    if registry.empty:
        st.warning(
            f"Файл реестра признаков не найден: {FEATURE_REGISTRY_FILE}"
        )
        return

    updates = edited_registry.set_index("feature")[
        ["display_name", "description"]
    ]

    for feature_name, row in updates.iterrows():
        mask = registry["feature"] == feature_name
        registry.loc[mask, "display_name"] = row["display_name"]
        registry.loc[mask, "description"] = row["description"]

    registry.to_csv(
        FEATURE_REGISTRY_FILE,
        index=False,
        encoding="utf-8-sig",
    )


def render_feature_selector(feature_set_name: str) -> list[str]:
    registry = load_feature_registry()

    if registry.empty:
        st.warning(
            f"Файл реестра признаков не найден: {FEATURE_REGISTRY_FILE}"
        )
        return []

    available_features = get_feature_set(feature_set_name)
    registry = registry[registry["feature"].isin(available_features)].copy()

    registry["display_name"] = registry["display_name"].fillna("")
    registry["description"] = registry["description"].fillna("")
    registry["source"] = registry["source"].fillna("OTHER")

    selection_key = f"selected_features::{feature_set_name}"
    editor_state_key = f"feature_editor_data::{feature_set_name}"
    current_set_key = "feature_editor_current_set"

    if selection_key not in st.session_state:
        st.session_state[selection_key] = available_features.copy()

    selected_features = set(st.session_state[selection_key])
    editor_frame = registry[
        [
            "status",
            "feature",
            "display_name",
            "description",
            "source",
        ]
    ].copy()
    editor_frame.insert(
        0,
        "selected",
        editor_frame["feature"].isin(selected_features),
    )

    if (
        current_set_key not in st.session_state
        or st.session_state[current_set_key] != feature_set_name
        or editor_state_key not in st.session_state
    ):
        st.session_state[current_set_key] = feature_set_name
        st.session_state[editor_state_key] = editor_frame.copy()

    st.caption(
        "Отмечайте признаки в таблице. Техническое имя не редактируется,"
        " а русское название и описание можно менять прямо здесь."
    )

    controls_left, controls_right = st.columns([1, 1])

    with controls_left:
        if st.button(
            "Выбрать все признаки",
            key=f"select_all::{feature_set_name}",
            width="stretch",
        ):
            updated = st.session_state[editor_state_key].copy()
            updated["selected"] = True
            st.session_state[editor_state_key] = updated
            st.session_state[selection_key] = available_features.copy()
            st.rerun()

    with controls_right:
        if st.button(
            "Снять все признаки",
            key=f"clear_all::{feature_set_name}",
            width="stretch",
        ):
            updated = st.session_state[editor_state_key].copy()
            updated["selected"] = False
            st.session_state[editor_state_key] = updated
            st.session_state[selection_key] = []
            st.rerun()

    edited_registry = st.data_editor(
        st.session_state[editor_state_key],
        key=f"feature_editor::{feature_set_name}",
        hide_index=True,
        width="stretch",
        height=520,
        column_config={
            "selected": column_config.CheckboxColumn(
                "Выбор",
                help="Отметьте признаки для обучения модели",
                width="small",
                default=True,
            ),
            "status": column_config.TextColumn(
                "Статус",
                width="small",
                disabled=True,
            ),
            "feature": column_config.TextColumn(
                "Техническое имя",
                width="medium",
                disabled=True,
            ),
            "display_name": column_config.TextColumn(
                "Русское название",
                width="large",
                required=False,
            ),
            "description": column_config.TextColumn(
                "Описание",
                width="large",
                required=False,
            ),
            "source": column_config.TextColumn(
                "Источник",
                width="medium",
                disabled=True,
            ),
        },
        disabled=["status", "feature", "source"],
    )

    st.session_state[editor_state_key] = edited_registry.copy()

    chosen_features = edited_registry.loc[
        edited_registry["selected"],
        "feature",
    ].tolist()
    st.session_state[selection_key] = chosen_features

    st.caption(
        f"Выбрано признаков: {len(chosen_features)} из {len(available_features)}"
    )

    if st.button(
        "Сохранить русские названия и описание",
        key=f"save_registry::{feature_set_name}",
        width="stretch",
    ):
        save_feature_registry_updates(edited_registry)
        st.success("Изменения в реестре признаков сохранены.")

    return chosen_features


def render_result_placeholder() -> None:
    st.markdown(
        """
        <div class="result-box empty-result">
            <div class="empty-icon">◆</div>
            <div class="empty-title">Готово к эксперименту</div>
            <div class="empty-text">
                Выберите модель и набор признаков<br>
                и нажмите «Запустить эксперимент»
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_history() -> None:
    st.markdown(
        '<div class="section-title">ИСТОРИЯ ЭКСПЕРИМЕНТОВ</div>',
        unsafe_allow_html=True,
    )

    if not (LOG_FILE.exists() and LOG_FILE.stat().st_size > 0):
        st.info("История пока пуста. Запустите первый эксперимент.")
        return

    history = pd.read_csv(LOG_FILE).sort_values(
        "start_time",
        ascending=False,
    )

    history_display = history[
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

    history_display.columns = [
        "Дата",
        "Модель",
        "Признаки",
        "GINI",
        "AUC",
        "Recall",
        "F1",
        "Время, сек.",
    ]

    st.dataframe(
        history_display,
        width="stretch",
        hide_index=True,
    )


render_header()

left, right = st.columns([1.0, 1.4], gap="medium")

from src.models import MODEL_NAMES

with left:
    st.markdown(
        '<div class="section-title">НАСТРОЙКИ ЭКСПЕРИМЕНТА</div>',
        unsafe_allow_html=True,
    )

    model_name = st.selectbox(
        "Модель",
        MODEL_NAMES,
    )

    feature_set = st.selectbox(
        "Набор признаков",
        [
            "BASE COMPACT",
            "BASE + SPARK",
        ],
    )

    if feature_set == "BASE COMPACT":
        st.markdown(
            """
            <div class="base-info">
                <b>38 исходных признаков</b>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="spark-info">
                <b>47 признаков:</b><br>
                BASE + 9 динамических SPARK
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(
            """
            <span class="spark-badge">+9 SPARK</span>
            """,
            unsafe_allow_html=True,
        )

    st.write("")
    run_button = st.button("▶  ЗАПУСТИТЬ ЭКСПЕРИМЕНТ")

selected_features = st.session_state.get(
    f"selected_features::{feature_set}",
    get_feature_set(feature_set),
)

with right:
    st.markdown(
        '<div class="section-title">ПРОГРЕСС ВЫПОЛНЕНИЯ</div>',
        unsafe_allow_html=True,
    )

    progress = st.progress(0)
    status = st.empty()

    st.write("")
    st.markdown(
        '<div class="section-title">РЕЗУЛЬТАТЫ</div>',
        unsafe_allow_html=True,
    )
    result_container = st.container()

    if run_button:
        try:
            status.markdown("### ◉ Подготовка данных...")
            progress.progress(10)

            status.markdown("### ◉ Загрузка TRAIN / TEST...")
            progress.progress(20)

            status.markdown(f"### ◉ Обучение {model_name}...")
            progress.progress(30)

            result = run_experiment(
                model_name=model_name,
                feature_set_name=feature_set,
                selected_features=selected_features,
            )

            status.markdown("### ◉ Расчёт метрик...")
            progress.progress(90)

            progress.progress(100)
            status.markdown("### ◉ Эксперимент завершён")

            auc = result["AUC"]
            gini = result["GINI"]
            recall = result["Recall"]
            f1 = result["F1"]
            runtime = result["elapsed_seconds"]

            with result_container:
                st.markdown(
                    f"""
                    <div class="result-box">
                        <b>{model_name}</b>
                        &nbsp;&nbsp;·&nbsp;&nbsp;
                        <b>{feature_set}</b>
                        &nbsp;&nbsp;·&nbsp;&nbsp;
                        <b>{result["n_features"]} признаков</b>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                c1, c2, c3, c4 = st.columns(4)
                metrics = [
                    (c1, "AUC", auc),
                    (c2, "GINI", gini),
                    (c3, "RECALL", recall),
                    (c4, "F1", f1),
                ]

                for column, label, value in metrics:
                    with column:
                        st.markdown(
                            f"""
                            <div class="metric-card">
                                <div class="metric-label">{label}</div>
                                <div class="metric-value">{value:.4f}</div>
                            </div>
                            """,
                            unsafe_allow_html=True,
                        )

                st.write("")
                st.info(
                    f"Использовано выбранных признаков: {result['n_features']} · "
                    f"Время выполнения: {runtime:.2f} сек. "
                    f"TRAIN: {result['train_size']:,} · "
                    f"TEST: {result['test_size']:,}"
                )

        except Exception as exc:
            status.markdown("### ◉ Ошибка выполнения")
            with result_container:
                st.error(f"Не удалось выполнить эксперимент: {exc}")
    else:
        status.caption("Ожидание запуска эксперимента")
        with result_container:
            render_result_placeholder()

st.write("")
st.markdown(
    '<div class="section-title">ВЫБОР ПРИЗНАКОВ</div>',
    unsafe_allow_html=True,
)
selected_features = render_feature_selector(feature_set)

st.write("")
render_history()
