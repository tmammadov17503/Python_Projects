import pandas as pd
import numpy as np

X = np.array([1000, 1500, 2000, 2500, 3000])
y = np.array([300000, 400000, 500000, 600000, 700000])

w_final = 200
b_final = 50000

y_pred = w_final * X + b_final

df = pd.DataFrame({
    "Size_sqft": X,
    "Price_actual": y,
    "Price_predicted": y_pred
})

df.to_csv("house_prices_predictions.csv", index=False)