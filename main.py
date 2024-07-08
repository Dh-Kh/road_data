from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (r2_score, mean_squared_error, 
                             mean_absolute_error)
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class RoadWim(object):
    
    @classmethod
    def log_reg(cls, path="data.csv"):
        df = pd.read_csv(path)        
        df = df.iloc[1:]
        x = df[["1"]].values
        y = df.drop(columns=["1"]).values
    
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.35, random_state=42) 
        l = LinearRegression()
        l.fit(x_train, y_train)
        y_pred = l.predict(x_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)
        mae = mean_absolute_error(y_test, y_pred)
        
        print(f'R-squared: {r2:.4f}')
        print(f'Mean Squared Error (MSE): {mse:.4f}')
        print(f'Root Mean Squared Error (RMSE): {rmse:.4f}')
        print(f'Mean Absolute Error (MAE): {mae:.4f}')
        
        plt.figure(figsize=(10, 6))
        sns.regplot(x=x_test[:, 0], y=y_test[:, 0], scatter_kws={"alpha": 0.5})
        plt.title("Actual vs. Predicted Values with Linear Regression")
        plt.xlabel("Feature (1)")
        plt.ylabel("Target Variable")
        plt.show()

        

def main():
    return RoadWim.log_reg()
    
if __name__ == "__main__":
    main()