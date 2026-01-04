# Food Prices Analysis and Machine Learning

## Project Overview
This repository contains data and code related to food prices across different countries and a machine learning model to analyze price trends.

## Files in this Repository

### 1. `Food Prices.csv`
- This dataset includes food price information by country, year, and month.
- **Columns:**
  - `Country`: The country where data was recorded.
  - `Year`: The year of the data.
  - `Month`: The month of the data.
  - `Food Item`: The name of the food product.
  - `Unit of Measurement`: The unit in which the food item is measured (e.g., Loaf for Bread).
  - `Average Price`: The average price of the item in the local currency.
  - `Currency`: The currency of the recorded price.
  - `Price in USD`: The price converted to US dollars.
  - `Availability`: Indicates the availability of the product.
  - `Quality`: The quality of the product (e.g., High, Medium, Low).

### 2. `MachiLearning (1).ipynb`
- A Jupyter Notebook that implements a machine learning model.
- It is designed to run in **Google Colab** as it includes Google Drive mounting.
- The notebook contains **17 code cells**, likely covering:
  - Data preprocessing and cleaning.
  - Exploratory Data Analysis (EDA).
  - Machine learning model training.
  - Predictions based on food price data.

## How to Use
1. Open `MachiLearning (1).ipynb` in Google Colab.
2. Ensure `Food Prices.csv` is accessible (upload it to Colab if necessary).
3. Run the notebook cells to process the data and analyze food price trends.

## Requirements
- Python (Jupyter Notebook)
- Pandas, NumPy, Matplotlib, and Machine Learning libraries (e.g., Scikit-learn)
- Google Colab (recommended for running the notebook)
