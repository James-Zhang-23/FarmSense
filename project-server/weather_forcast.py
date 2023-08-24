import requests, json
import pickle
from sklearn.linear_model import LogisticRegression

api_key = "9f27246f277709f54e3de00c0aa92397"

base_url = "https://api.openweathermap.org/data/2.5/forecast?"

lat = "34.0262195"
lon = "-118.2877426"

units = "metric"

cnt = "24"

complete_url = base_url + "lat=" + lat + "&lon=" + lon + "&cnt="+ cnt + "&units=" + units + "&appid=" + api_key

def get_weather_forecast():
    # get http response
    response = requests.get(complete_url)

    # convert json format data into python format data
    rawData = response.json()

    # get all temperature and humidity value to a list
    temperature_list = []
    humidity_list = []

    if rawData["cod"] != "404":
        weather = rawData["list"]
        
        for i in range(len(weather)):
            temperature_list.append(weather[i]['main']['temp'])
            humidity_list.append(weather[i]['main']['humidity'])
    
    future_temp_mean = sum(temperature_list) / len(temperature_list)
    future_hum_mean = sum(humidity_list) / len(humidity_list)
    return (future_temp_mean, future_hum_mean)

def create_suggetion(future_weather, mean_data):
    # get useful data
    soil_hum_mean = mean_data.get('soil_humidity_mean')
    air_temp_mean = mean_data.get('air_temperature_mean')
    air_hum_mean = mean_data.get('air_humidity_mean')
    future_temp = future_weather[0]
    future_hum = future_weather[1]

    # load pre-trained model
    water_model = pickle.load(open("water_suggest_ann.pickle", "rb"))
    roof_model = pickle.load(open("roof_suggest_ann.pickle", "rb"))
    
    # predict
    test_data = [soil_hum_mean, air_temp_mean, air_hum_mean, future_temp, future_hum]
    water_suggest = water_model.predict([test_data])
    roof_suggest = roof_model.predict([test_data])
    
    return (water_suggest[0], roof_suggest[0])



if __name__ == "__main__":
    future_weather = get_weather_forecast()
    print(future_weather)
