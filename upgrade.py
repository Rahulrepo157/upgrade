# -*- coding: utf-8 -*-
"""UPGRADE.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1pHUt7wNIbGvQOAjzSFOlRWZ1E65BjZBj
"""

import pandas as pd
import numpy as np

data=pd.read_csv("day.csv")

data.head()

import warnings
warnings.filterwarnings('ignore')

data.info()

data.describe()

import matplotlib.pyplot as plt
import seaborn as sns



sns.pairplot(data)
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

# Set up the figure
plt.figure(figsize=(40, 30))

# Boxplots for each categorical variable
categorical_vars = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']

for i, var in enumerate(categorical_vars, 1):
    plt.subplot(2, 4, i)  # Create a subplot grid (2 rows, 4 columns)
    sns.boxplot(data=data, x=var, y='cnt', palette='Set2')
    plt.title(f'Boxplot of {var} vs cnt', fontsize=14)
    plt.xlabel(var, fontsize=12)
    plt.ylabel('Count (cnt)', fontsize=12)

# Adjust layout for better visualization
plt.tight_layout()
plt.show()

#since year month and weekday ios already given drop the dteday
#we also do not need index for our model building hence drop this column is well(instant)
# Drop the 'instant' and 'dteday' columns
data = data.drop(columns=['instant', 'dteday'])

# Verify the updated DataFrame
data.head()

# List of categorical variables
categorical_vars = ['season', 'yr', 'mnth', 'holiday', 'weekday', 'workingday', 'weathersit']

# Automate value counts
for var in categorical_vars:
    print(f"Value counts for '{var}':")
    print(data[var].value_counts())
    print("\n" + "-"*50 + "\n")

# List of variables for which dummies need to be created (excluding binary variables)
categorical_vars = ['season', 'mnth', 'weekday', 'weathersit']

# Create dummy variables and drop the first column of each for reference (to avoid multicollinearity)
data_with_dummies = pd.get_dummies(data,columns=categorical_vars,drop_first=True)

# Check the updated DataFrame
print(data_with_dummies.head())

data_with_dummies.info()

for col in data_with_dummies.columns:
    if data_with_dummies[col].dtype == 'bool':  # Check if the column is of boolean type
        data_with_dummies[col] = data_with_dummies[col].astype(int)

# Check the data after conversion
print(data_with_dummies.head())

data_with_dummies



from sklearn.model_selection import train_test_split
df_train,df_test=train_test_split(data_with_dummies,train_size=0.7,test_size=0.3,random_state=100)

data_with_dummies.head()

data_with_dummies.info()

data_with_dummies.shape

data_with_dummies.columns

from sklearn.preprocessing import MinMaxScaler as sc

scalar=sc()

variables_list = [ 'temp',
                    'atemp',
                    'hum',
                    'registered',
                    'cnt']

df_train[variables_list]=scalar.fit_transform(df_train[variables_list])

df_train[variables_list].info()

df_train.describe()

#find the correlation of all the variables in the traning dataset
plt.figure(figsize=(50,30))
sns.heatmap(df_train.corr(),annot=True,cmap="YlGnBu")
plt.show()

import numpy as np

# Calculate the correlation matrix
corr_matrix = df_train.corr()

# Set a threshold for high correlation
threshold = 0.85

# Find variable pairs with high correlation
high_corr_pairs = np.where(np.abs(corr_matrix) > threshold)
high_corr_indices = [(corr_matrix.index[x], corr_matrix.columns[y])
                     for x, y in zip(*high_corr_pairs) if x != y and x < y]

# Print highly correlated pairs
print("Highly correlated feature pairs:")
for pair in high_corr_indices:
    print(pair)

plt.figure(figsize=[6,6])
plt.scatter(df_train.registered, df_train.cnt)
plt.show()

#since rtegestered is the highly correlated variable with the cnt hence we will chosse this as a predictor varible and build a model
y_train = df_train.pop('cnt')
X_train = df_train

X_train

import statsmodels.api  as sm
x_trainlm=sm.add_constant(X_train["registered"])
lm=sm.OLS(y_train,x_trainlm).fit()
print(lm.summary())

lm.params

"""adding another variable to see if there any increse in adjusted r2"""

import statsmodels.api  as sm
x_trainlm=sm.add_constant(X_train[["registered","casual"]])
lm=sm.OLS(y_train,x_trainlm).fit()
print(lm.summary())

import statsmodels.api  as sm
x_trainlm=sm.add_constant(X_train[["atemp","yr","registered","casual"]])
lm=sm.OLS(y_train,x_trainlm).fit()
print(lm.summary())

import statsmodels.api  as sm
x_trainlm=sm.add_constant(X_train)
lm=sm.OLS(y_train,x_trainlm).fit()
print(lm.summary())

# Check for the VIF values of the feature variables.
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X_train.columns
vif['VIF'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X_train.drop('workingday',axis=1)

print(X)

# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()

print(lr_2.summary())

# Check for the VIF values of the feature variables.
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X_train.columns
vif['VIF'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('holiday',axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

# Check for the VIF values of the feature variables.
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X_train.columns
vif['VIF'] = [variance_inflation_factor(X_train.values, i) for i in range(X_train.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('yr', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('workingday', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('mnth_7', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('mnth_3', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('mnth_6', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('hum', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('mnth_10', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

# Dropping highly correlated variables and insignificant variables
X = X.drop('yr', axis=1)
# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

variables_to_drop = [
    'holiday', 'temp', 'atemp', 'windspeed', 'season_2', 'season_3',
    'season_4', 'mnth_2', 'mnth_4', 'mnth_5', 'mnth_8', 'mnth_9',
    'mnth_11', 'mnth_12', 'weekday_1', 'weekday_2', 'weekday_3',
    'weekday_4', 'weekday_5', 'weekday_6', 'weathersit_2', 'weathersit_3'
]

# Dropping variables from X_train
X = X.drop(variables_to_drop, axis=1)

# Build a third fitted model
X_train_lm = sm.add_constant(X)

lr_2 = sm.OLS(y_train, X_train_lm).fit()
print(lr_2.summary())

from statsmodels.stats.outliers_influence import variance_inflation_factor
vif = pd.DataFrame()
vif['Features'] = X.columns
vif['VIF'] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
vif['VIF'] = round(vif['VIF'], 2)
vif = vif.sort_values(by = "VIF", ascending = False)
vif

y_train_price = lr_2.predict(X_train_lm)

fig = plt.figure()
sns.distplot((y_train - y_train_price), bins = 20)
fig.suptitle('Error Terms', fontsize = 20)                  # Plot heading
plt.xlabel('Errors', fontsize = 18)

num_vars = ['temp', 'atemp', 'hum', 'casual', 'cnt','registred']

df_test[num_vars] = .transform(df_test[num_vars])
df_test.describe()

data

