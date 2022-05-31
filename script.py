# Rent Prediction – Use of Multiple Linear Regression machine learning model to predict Manhattan rent prices given inputs
# Multiple Linear Regression uses two or more independent variables to predict the values of the dependent variable.

import pandas as pd
import numpy as np

# import the dataset of various apartments in manhattan, their features and rent price
apartments = pd.read_csv("updated_apartments.csv")

# load the data into a pandas dataframe for manipulation, view the data
df = pd.DataFrame(apartments)
# print(df.head())

# As with most machine learning algorithms, we have to split our dataset into:
# Training set: the data used to fit the model
# Test set: the data partitioned away at the very start of the experiment (to provide an unbiased evaluation of the model)
# In general, putting 80% of your data in the training set and 20% of your data in the test set is a good place to start.
from sklearn.model_selection import train_test_split

# set x as all of input values
x = df[['bedrooms', 'bathrooms', 'size_sqft']]
print("x is ")
print(x.head())

# set y as all of output to predict: rent
y = df[['rent']]
print("y is ")
print(y.head())

# split x into 80% training and 20% testing
x_train, x_test, y_train, y_test = train_test_split(x, y, train_size = 0.8, test_size = 0.2, random_state=6)

# show the shape of the x arrays
print("x_train array shape is ")
print(x_train.shape)
print("x_test array shape is ")
print(x_test.shape)

# show the shape of the rent
print("y_train array shape is ")
print(y_train.shape)
print("y_test array shape is ")
print(y_test.shape)

from sklearn.linear_model import LinearRegression

# set mlr as our multiple regression model
mlr = LinearRegression()

# fit in x train and y train arrays into this 3d arrray, use .values so we remove header
model = mlr.fit(x_train.values, y_train.values)

# create new demo room with following criterias: 1 bedroom, 1 bath and 800 sqft
given_attributes = [[1, 1, 800]]

# predict y (rent) given all of x values (apartment attributes)
predicted_rent = mlr.predict(given_attributes)

print("The predicted rent is: $%.2f" % predicted_rent)
# the predicted amount is $4205.27
# Therefore we know to look for apartments less than this amount with the given criterias.

# for all the visualizations
import matplotlib.pyplot as plt

# plot scatters to show a few attributes and their correlation with price

plt.scatter(df[['size_sqft']], df[['rent']], alpha=0.4)
plt.title("sqft correlation with price")
plt.show()
# seems to be a positive correlation between sqft and price

plt.scatter(df[['bathrooms']], df[['rent']], alpha=0.4)
plt.title("bathrooms correlation with price")
plt.show()
# seems to be a positive correlation between bathrooms and price

plt.scatter(df[['bedrooms']], df[['rent']], alpha=0.4)
plt.title("bedrooms correlation with price")
plt.show()
# seems to be a positive correlation between bedrooms and price

plt.scatter(df[['min_to_subway']], df[['rent']], alpha=0.4)
plt.title("minutes-to-subway correlation with price")
plt.show()
# seems to be a slightly positive correlation between floor height and price



# create a heatmap to show correlations between all attributes 
import seaborn as sns

#Use the `.corr()` method on `df` to get the correlation matrix 
correlation_matrix = df.corr()

# create heatmap, set hues for negative, positive areas of map and saturation amount.
# create heatmap given: dataset, value range to anchor map with (-1 and 1), colarmap name set above, set title
red_blue = sns.diverging_palette(220, 20, as_cmap=True)
sns.heatmap(correlation_matrix, vmin = -1, vmax = 1, cmap=red_blue).set(title="Correlation Heatmap")
plt.show()


# now we compare our predicted values against our 20% test values we pulled out earlier
# this tells us hows close our rent prediction is to actuals 
# predict y given x_test this time, instead of x_train
y_predict = mlr.predict(x_test)

# view the tables
view_y_predict = pd.DataFrame(y_predict)
print("y predict is ")
print(view_y_predict.head())

view_y_test = pd.DataFrame(y_test)
print("y test is ")
print(view_y_test.head())

print("y_predict array shape is ")
print(y_predict.shape)

print("y_test array shape is ")
print(y_test.shape)

# both shapes should be the same as there should be the same amount of Y-predict given x_tests as y_tests

# plot actual vs predicted rent prices:
# x-axis is actual, y-axis is predicted

# plot y_tests vs y_predicts , 0.4 transparency level
plt.scatter(y_test, y_predict, alpha=0.4)
plt.xlabel("Actual Prices: ")
plt.ylabel("Predicted prices: ")
plt.title("Actual Rent vs Predicted Rent")
plt.show()

# seems to be an accurate prediction, but how close exactly?
# evaluating accuracy using Residual Analysis:
# The difference between the actual y, and the predicted y is the residual e. e=y-Y^
# R^2, residual sum of squares divided by total sum of squares and tells us variation in the y variable
# .77 means that all x variables together explain 77% variation in y.
# 3 x variables (sqft ft, bedrooms and age) might explain 95% of the variation in rent. 
# typically the more x variables we add, the higher the score should be
# 1 is best possible, 0.7 is considered good. 

# find train score below
print("Train score:")
print(mlr.score(x_train, y_train))
# our R^2 for training set is .77 

print("Test score:")
print(mlr.score(x_test, y_test))
# our R^2 for test set is .80 

# residuals = predicted rent prices - actual rent prices
residuals = y_predict - y_test

# view residuals
view_residuals = pd.DataFrame(residuals)
print("residuals is ")
print(view_residuals.head())

plt.scatter(y_predict, residuals, alpha=0.4)
plt.xlabel("Predicted rent prices")
plt.ylabel("Residual amount")
plt.title('Residual Analysis')
 
plt.show()
# we can see the variation among predicted and actual prices as rent goes higher, it becomes harder to predict
