import pandas as pd

from ml_ops_project.fe import build_preprocess


def test_build_preprocess_fit_transform():
    df = pd.DataFrame({"f1": [1.0, 2.0, 3.0], "city": ["a", "b", "a"]})
    prep = build_preprocess(df)
    Xt = prep.fit_transform(df)
    assert hasattr(Xt, "shape")
    assert Xt.shape[0] == 3
    assert Xt.shape[1] >= 2
