import pandas as pd

from ml_ops_project.data_utils import load_csv


def test_load_csv(tmp_path):
    csv_data = "a,b\n1,2\n3,4\n"
    f = tmp_path / "test.csv"
    f.write_text(csv_data)
    df = load_csv(f)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)
