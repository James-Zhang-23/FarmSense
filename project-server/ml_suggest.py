import pandas
from sklearn.neural_network import MLPClassifier
import pickle

data = pandas.read_csv("data.csv")

X = data[['soil_hum', 'air_temp', 'air_hum', 'future_temp', 'future_hum']]
Y = data['water']
Z = data['roof']

# ANN configuration
hidden_layer_sizes = (20, 20)  # Two hidden layers with 20 neurons each
activation = 'relu'
solver = 'adam'
max_iter = 10000
alpha = 1e-4

# Create and train the ANNs
water_ann = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, 
                          solver=solver, alpha=alpha, max_iter=max_iter)
water_ann.fit(X.values, Y.values)

roof_ann = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, activation=activation, 
                         solver=solver, alpha=alpha, max_iter=max_iter)
roof_ann.fit(X.values, Z.values)

"""
water_suggest = water_ann.predict([[38.2, 21.5, 35.1, 12.5, 42.2]])
roof_suggest = roof_ann.predict([[38.2, 21.5, 35.1, 12.5, 42.2]])
"""

filename1 = "water_suggest_ann.pickle"
filename2 = "roof_suggest_ann.pickle"

# Save models
pickle.dump(water_ann, open(filename1, "wb"))
pickle.dump(roof_ann, open(filename2, "wb"))

