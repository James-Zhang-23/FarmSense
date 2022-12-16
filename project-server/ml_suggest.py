import pandas
from sklearn.linear_model import LogisticRegression
import pickle

data = pandas.read_csv("data.csv")

X = data[['soil_hum', 'air_temp', 'air_hum', 'future_temp', 'future_hum']]
Y = data['water']
Z = data['roof']

# multinomial logistic regression
water_logreg = LogisticRegression(max_iter=10000, C=2)
water_logreg.fit(X.values,Y.values)

roof_logreg = LogisticRegression(max_iter=10000, C=2)
roof_logreg.fit(X.values,Z.values)

"""
water_suggest = water_logreg.predict([[38.2,21.5,35.1,12.5,42.2]])
roof_suggest = roof_logreg.predict([[38.2,21.5,35.1,12.5,42.2]])
"""

filename1 = "water_suggest.pickle"
filename2 = "roof_suggest.pickle"

# save model
pickle.dump(water_logreg, open(filename1, "wb"))
pickle.dump(roof_logreg, open(filename2, "wb"))
