import pandas as pd
import streamlit as st
from sklearn.datasets import load_diabetes, load_iris
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

from .paths import REFERENCE_DIR


def get_dataset(task):
    if task == "Classification":
        dataset = load_iris(as_frame=True)
        return dataset.data, dataset.target, list(dataset.target_names), "Iris"
    dataset = load_diabetes(as_frame=True)
    return dataset.data, dataset.target, None, "Diabetes"


def build_model(task, model_name, random_state):
    if task == "Classification":
        if model_name == "Logistic regression":
            estimator = LogisticRegression(max_iter=1000, random_state=random_state)
            return make_pipeline(StandardScaler(), estimator)
        if model_name == "K-nearest neighbors":
            return make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
        return RandomForestClassifier(n_estimators=200, random_state=random_state)

    if model_name == "Ridge regression":
        return make_pipeline(StandardScaler(), Ridge(alpha=1.0))
    if model_name == "Random forest regressor":
        return RandomForestRegressor(n_estimators=200, random_state=random_state)
    return make_pipeline(StandardScaler(), LinearRegression())


def scikit_learn_cheatsheet():
    st.set_page_config(page_title="CheatSheets | Scikit-learn", page_icon=":material/auto_stories:", layout="wide")
    reference_file = REFERENCE_DIR / "scikit_learn_cheatsheet.md"
    if not reference_file.is_file():
        st.error(f"Reference file not found: {reference_file.name}")
        st.stop()

    st.title("Scikit-learn cheatsheet")
    reference_tab, playground_tab = st.tabs(["Cheatsheet", "Model playground"])

    with reference_tab:
        st.download_button(
            "Download reference",
            data=reference_file.read_bytes(),
            file_name=reference_file.name,
            mime="text/markdown",
            icon=":material/download:",
        )
        st.markdown(reference_file.read_text(encoding="utf-8"))

    with playground_tab:
        task = st.selectbox("Task", ["Classification", "Regression"], key="sklearn_task")
        model_options = (
            ["Logistic regression", "K-nearest neighbors", "Random forest classifier"]
            if task == "Classification"
            else ["Linear regression", "Ridge regression", "Random forest regressor"]
        )
        control_columns = st.columns(3)
        model_name = control_columns[0].selectbox("Model", model_options, key="sklearn_model")
        test_size = control_columns[1].slider("Test data", 0.1, 0.4, 0.2, 0.05, key="sklearn_test_size")
        random_state = control_columns[2].number_input("Random seed", min_value=0, value=42, step=1, key="sklearn_random_state")
        X, y, target_names, dataset_name = get_dataset(task)
        st.caption(f"Dataset: {dataset_name} · {len(X)} rows · {len(X.columns)} features")

        if st.button("Train and evaluate", icon=":material/play_arrow:", key="train_sklearn_model"):
            stratify = y if task == "Classification" else None
            X_train, X_test, y_train, y_test = train_test_split(
                X,
                y,
                test_size=test_size,
                random_state=int(random_state),
                stratify=stratify,
            )
            model = build_model(task, model_name, int(random_state))
            model.fit(X_train, y_train)
            predictions = model.predict(X_test)
            results = pd.DataFrame({"Actual": y_test.to_numpy(), "Predicted": predictions})

            st.session_state["sklearn_results"] = results
            st.session_state["sklearn_task_result"] = task
            if task == "Classification":
                st.session_state["sklearn_accuracy"] = accuracy_score(y_test, predictions)
                matrix = confusion_matrix(y_test, predictions)
                st.session_state["sklearn_confusion"] = pd.DataFrame(
                    matrix,
                    index=target_names,
                    columns=target_names,
                )
                st.session_state["sklearn_report"] = pd.DataFrame(
                    classification_report(
                        y_test,
                        predictions,
                        target_names=target_names,
                        output_dict=True,
                        zero_division=0,
                    )
                ).transpose()
            else:
                st.session_state["sklearn_mae"] = mean_absolute_error(y_test, predictions)
                st.session_state["sklearn_rmse"] = root_mean_squared_error(y_test, predictions)
                st.session_state["sklearn_r2"] = r2_score(y_test, predictions)

        if st.session_state.get("sklearn_task_result") == "Classification":
            st.metric("Test accuracy", f"{st.session_state['sklearn_accuracy']:.1%}")
            st.markdown("**Confusion matrix**")
            st.dataframe(st.session_state["sklearn_confusion"], width="stretch")
            st.markdown("**Classification report**")
            st.dataframe(st.session_state["sklearn_report"], width="stretch")
        elif st.session_state.get("sklearn_task_result") == "Regression":
            metric_columns = st.columns(3)
            metric_columns[0].metric("Mean absolute error", f"{st.session_state['sklearn_mae']:.3f}")
            metric_columns[1].metric("Root mean squared error", f"{st.session_state['sklearn_rmse']:.3f}")
            metric_columns[2].metric("R²", f"{st.session_state['sklearn_r2']:.3f}")

        if "sklearn_results" in st.session_state:
            st.markdown("**Holdout predictions**")
            st.dataframe(st.session_state["sklearn_results"], hide_index=True, width="stretch")
            st.download_button(
                "Download predictions",
                data=st.session_state["sklearn_results"].to_csv(index=False).encode("utf-8"),
                file_name="scikit_learn_predictions.csv",
                mime="text/csv",
                icon=":material/download:",
            )
