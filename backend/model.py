import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from backend.preprocess import get_feature_matrix, get_target_vector, FEATURE_COLUMNS


def train_model(df, random_state=42):
    X = get_feature_matrix(df)
    y = get_target_vector(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.25,
        random_state=random_state
    )

    model = RandomForestClassifier(
        n_estimators=120,
        random_state=random_state
    )
    model.fit(X_train, y_train)

    accuracy = model.score(X_test, y_test)
    return model, accuracy


def predict_risk(model, input_df):
    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]
    return prediction, probabilities


def get_feature_importance(model):
    feature_importance = pd.DataFrame({
        "Feature": FEATURE_COLUMNS,
        "Importance": model.feature_importances_
    }).sort_values("Importance", ascending=False)
    return feature_importance