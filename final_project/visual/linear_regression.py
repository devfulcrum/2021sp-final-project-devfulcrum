import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression


def visual_demo():
    """

    This is to perform a linear regression and visualize the data

    :return:
        The generated visuals as output for validations and testing.

    """
    data = \
        [
            [0, 340000],
            [1, 350000],
            [2, 320000],
            [3, 360000],
            [4, 380000],
            [5, 390000],
            [6, 400000],
            [7, 390000],
        ]
    X = np.array(data)[:, 0].reshape(-1, 1)
    y = np.array(data)[:, 1].reshape(-1, 1)
    print("X=")
    print(X)
    print("y=")
    print(y)

    to_predict_x = [8, 9, 10]
    to_predict_x = np.array(to_predict_x).reshape(-1, 1)

    lin_reg = LinearRegression()
    lin_reg.fit(X, y)

    predicted_y = lin_reg.predict(to_predict_x)
    m = lin_reg.coef_
    c = lin_reg.intercept_
    print("Predicted y:\n", predicted_y)
    rounded_pred = [[round(num) for num in predicted_y[0]][0],
                    [round(num) for num in predicted_y[1]][0],
                    [round(num) for num in predicted_y[2]][0]]
    print("rounded :\n", rounded_pred)
    print("rounded :\n", [round(num) for num in predicted_y[0]])
    print("rounded :\n", [round(num) for num in predicted_y[1]])
    print("rounded :\n", [round(num) for num in predicted_y[2]])
    print("slope (m): ", m)
    print("y-intercept (c): ", c)

    plt.title('Predict the next numbers in a given sequence')
    plt.xlabel('X')
    plt.ylabel('Numbers')
    plt.scatter(X, y, color="blue")
    new_y = [m * i + c for i in np.append(X, to_predict_x)]
    new_y = np.array(new_y).reshape(-1, 1)
    plt.plot(np.append(X, to_predict_x), new_y, color="red")
    plt.show()

    return


if __name__ == "__main__":
    """
    For running locally and validating the visuals that can be implemented
    """
    visual_demo()
