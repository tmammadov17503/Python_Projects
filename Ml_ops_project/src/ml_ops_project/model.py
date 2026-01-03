from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


def build_model(preprocess) -> Pipeline:
    clf = RandomForestClassifier(n_estimators=300, random_state=42)
    return Pipeline([("prep", preprocess), ("clf", clf)])
