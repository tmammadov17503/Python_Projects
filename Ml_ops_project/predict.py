import argparse
from pathlib import Path

import pandas as pd
from joblib import load

from src.ml_ops_project.data_utils import load_csv


def main(args):
    model = load(args.model_path)
    df = load_csv(args.input_csv)
    preds = model.predict(df)
    out = pd.DataFrame({"prediction": preds})
    Path(args.out_csv).parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out_csv, index=False)
    print(f"Wrote predictions to {args.out_csv}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--model_path", default="models/model.joblib")
    p.add_argument("--input_csv", required=True)
    p.add_argument("--out_csv", default="predictions/preds.csv")
    main(p.parse_args())
