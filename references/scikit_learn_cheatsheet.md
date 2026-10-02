# Scikit-learn Quick Reference

## Split and preprocess data

```python
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = make_pipeline(StandardScaler(), estimator)
```

Use `stratify=y` for classification splits so class proportions are kept similar. Fit preprocessing inside a pipeline to avoid leaking test data into training.

## Classification

```python
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(accuracy_score(y_test, predictions))
print(classification_report(y_test, predictions))
```

Other common classifiers include `KNeighborsClassifier`, `RandomForestClassifier`, and `SVC`.

## Regression

```python
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, r2_score

model = make_pipeline(StandardScaler(), Ridge(alpha=1.0))
model.fit(X_train, y_train)
predictions = model.predict(X_test)
print(mean_absolute_error(y_test, predictions))
print(r2_score(y_test, predictions))
```

Other common regressors include `LinearRegression`, `RandomForestRegressor`, and `HistGradientBoostingRegressor`.

## Model selection

```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
print(scores.mean(), scores.std())
```

For regression, use a metric such as `neg_mean_absolute_error` or `r2` instead of `accuracy`.

## Tune parameters

```python
from sklearn.model_selection import GridSearchCV

search = GridSearchCV(model, {"ridge__alpha": [0.1, 1.0, 10.0]}, cv=5)
search.fit(X_train, y_train)
print(search.best_params_)
```

## Save a trained model

```python
import joblib

joblib.dump(model, "model.joblib")
loaded_model = joblib.load("model.joblib")
```

The playground uses the built-in Iris classification and Diabetes regression datasets and keeps the test split separate from training.