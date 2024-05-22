import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
from pandas_datareader.famafrench import get_available_datasets
from pandas_datareader.data import DataReader


# Function to fetch Fama-French 3-factor model dataset
def fetch_fama_french_factors():
    datasets = get_available_datasets()
    ff_dataset = "F-F_Research_Data_Factors_daily"
    if ff_dataset in datasets:
        ff_data = DataReader(ff_dataset, "famafrench", start="2010-01-01")[0]
        ff_data.columns = ["Market", "SMB", "HML", "RF"]
        return ff_data
    else:
        raise ValueError("Fama-French 3-factor model data not available.")


# Simulate some asset returns (replace this with your asset's data)
def simulate_asset_returns(ff_data):
    np.random.seed(0)
    asset_returns = ff_data["Market"] + np.random.normal(0, 0.5, size=len(ff_data))
    return asset_returns


# Perform regression analysis
def perform_regression(ff_data, asset_returns):
    X = ff_data[["Market", "SMB", "HML"]]
    X = sm.add_constant(X)  # Adding a constant for the intercept
    y = asset_returns - ff_data["RF"]  # Subtract the risk-free rate

    model = sm.OLS(y, X)
    results = model.fit()
    return results


# Function to plot regression results and evaluate the model
def plot_and_evaluate(results, ff_data, asset_returns):
    # Plotting the actual vs predicted returns
    predicted_returns = results.predict(
        sm.add_constant(ff_data[["Market", "SMB", "HML"]])
    )
    plt.figure(figsize=(10, 6))
    plt.scatter(asset_returns, predicted_returns, alpha=0.5)
    plt.plot(
        [asset_returns.min(), asset_returns.max()],
        [asset_returns.min(), asset_returns.max()],
        "r--",
    )
    plt.xlabel("Actual Returns")
    plt.ylabel("Predicted Returns")
    plt.title("Actual vs Predicted Returns")
    plt.show()

    # Printing the summary of the regression results
    print(results.summary())


# Main function to run the analysis
def main():
    ff_data = fetch_fama_french_factors()
    asset_returns = simulate_asset_returns(ff_data)
    results = perform_regression(ff_data, asset_returns)
    plot_and_evaluate(results, ff_data, asset_returns - ff_data["RF"])


if __name__ == "__main__":
    main()
