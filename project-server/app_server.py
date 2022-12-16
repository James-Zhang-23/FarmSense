from flask import Flask,jsonify,request
import boto3
import credentials as keys
from boto3.dynamodb.conditions import Key, Attr
from flask_apscheduler import APScheduler
import json
import time
import get_mean
import get_latest
import send_email
import weather_forcast

# warning boundary
MAX_AIR_TEMPERATURE = 40
MIN_AIR_TEMPERATURE = 10
MAX_AIR_HUMIDITY = 70
MIN_AIR_HUMIDITY = 30
MAX_AIR_PRESSURE = 120
MIN_AIR_PRESSURE = 90
MAX_SOIL_TEMPERATURE = 35
MIN_SOIL_TEMPERATURE = 10
MAX_SOIL_HUMIDITY = 60
MIN_SOIL_HUMIDITY = 20


# Get the dynamoDB resource
dynamodb = boto3.resource('dynamodb',
                    aws_access_key_id=keys.ACCESS_KEY_ID,
                    aws_secret_access_key=keys.ACCESS_SECRET_KEY,
                    region_name=keys.AWS_DEFAULT_REGION)

table = dynamodb.Table('sensor_2')


# scheduled job function
def mail_notification():
    # get current time
    timestamp = int(time.time()*1000)
    # make it 30 seconds before
    timestamp = timestamp - 30000

    # get the data from DynamoDB
    response = table.scan(
        FilterExpression=Attr('time').gt(str(timestamp))
    )
    items = response['Items']

    # get mean data
    mean_data = get_mean.get_mean_data(items)

    #compare with boundary and build msg
    msg = ""
    if mean_data.get("air_temperature_mean") > MAX_AIR_TEMPERATURE:
        msg = msg + "air temperature exceed limit; "
    if mean_data.get("air_temperature_mean") < MIN_AIR_TEMPERATURE:
        msg = msg + "air temperature below limit; "
    if mean_data.get("air_humidity_mean") > MAX_AIR_HUMIDITY:
        msg = msg + "air humidity exceed limit; "
    if mean_data.get("air_humidity_mean") < MIN_AIR_HUMIDITY:
        msg = msg + "air humidity below limit; "
    if mean_data.get("soil_temperature_mean") > MAX_SOIL_TEMPERATURE:
        msg = msg + "soil temperature exceed limit; "
    if mean_data.get("soil_temperature_mean") < MIN_SOIL_TEMPERATURE:
        msg = msg + "soil temperature below limit; "
    if mean_data.get("soil_humidity_mean") > MAX_SOIL_HUMIDITY:
        msg = msg + "soil humidity exceed limit; "
    if mean_data.get("soil_humidity_mean") < MIN_SOIL_HUMIDITY:
        msg = msg + "soil humidity below limit; "
    
    if msg != "":
        send_email.send_plain_email(msg)


# set configuration values
class Config:
    JOBS = [
        {
            "id": "job1",
            "func": mail_notification,
            "trigger": "interval",
            "seconds": 60,
        }
    ]
    SCHEDULER_API_ENABLED = True


# create app
app = Flask(__name__)
app.config.from_object(Config())


# initialize scheduler
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()


# Start backend server
@app.route('/')
def index():
    return 'Flask server is up'


# Get sensor data after the timestamp
# return in JSON format
@app.route('/getdata')
def getdata():
    # get current time
    timestamp = int(time.time()*1000)
    # make it 30 seconds before
    timestamp = timestamp - 30000

    response = table.scan(
        FilterExpression=Attr('time').gt(str(timestamp))
    )
    items = response['Items']

    # get latest data from the respond data(30s)
    latest_data = get_latest.get_latest_data(items)

    # convert to json format
    latest_data_json = jsonify(latest_data)

    return latest_data_json


# Get suggestion
# return in JSON farmat
@app.route('/suggestion')
def suggestion():
    # get current time
    timestamp = int(time.time()*1000)
    # make it 120 seconds before
    timestamp = timestamp - 120000

    # get the data from DynamoDB
    response = table.scan(
        FilterExpression=Attr('time').gt(str(timestamp))
    )
    items = response['Items']

    # get mean data
    mean_data = get_mean.get_mean_data(items)

    # get weather forecast for 3 days
    future_weather = weather_forcast.get_weather_forecast()

    # make suggestion based on mean and forecast
    suggestion = weather_forcast.create_suggetion(future_weather, mean_data)
    
    # convert suggest to json
    suggestion_dict = {}
    suggestion_dict["water"] = int(suggestion[0])
    suggestion_dict["roof"] = int(suggestion[1])
    suggestion_json = jsonify(suggestion_dict)

    return suggestion_json


# use gunicorn to deploy
# gunicorn --bind 0.0.0.0:5000 app_server:app
if __name__ == '__main__':
    app.run(host='0.0.0.0')