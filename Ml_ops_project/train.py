import argparse
import json
from pathlib import Path

from joblib import dump
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from src.ml_ops_project.data_utils import load_csv
from src.ml_ops_project.fe import build_preprocess
from src.ml_ops_project.model import build_model


def main(args):
    df = load_csv(args.train_csv)
    y = df[args.target]
    X = df.drop(columns=[args.target])

    preprocess = build_preprocess(X)
    pipe = build_model(preprocess)

    # safer split for tiny demo data
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.4, random_state=42)
    pipe.fit(X_tr, y_tr)
    preds = pipe.predict(X_te)
    acc = accuracy_score(y_te, preds)

    Path(args.model_out).parent.mkdir(parents=True, exist_ok=True)
    dump(pipe, args.model_out)

    Path(args.metrics_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.metrics_out).write_text(json.dumps({"accuracy": acc}, indent=2))
    print(f"Saved model to {args.model_out}; accuracy={acc:.4f}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--train_csv", required=True)
    p.add_argument("--target", required=True)
    p.add_argument("--model_out", default="models/model.joblib")
    p.add_argument("--metrics_out", default="models/metrics.json")
    main(p.parse_args())
