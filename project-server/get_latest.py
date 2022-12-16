def get_latest_data(list_data):
    air_temperature_latest = 0.0
    air_humidity_latest = 0.0
    air_pressure_latest = 0.0
    soil_humidity_latest = 0.0
    soil_temperature_latest = 0.0
    latest_time_air = 0
    latest_time_soil = 0

    for sensor_data in list_data:
        if sensor_data.get("air_temperature") is not None:
            if int(sensor_data.get("time")) >= latest_time_air:
                latest_time_air = int(sensor_data.get("time"))
                air_temperature_latest = float(sensor_data.get("air_temperature"))
                air_humidity_latest = float(sensor_data.get("air_humidity"))
                air_pressure_latest = float(sensor_data.get("air_pressure"))
        else:
            if int(sensor_data.get("time")) >= latest_time_soil:
                latest_time_soil = int(sensor_data.get("time"))
                soil_temperature_latest = float(sensor_data.get("soil_temperature"))
                soil_humidity_latest = float(sensor_data.get("soil_humidity"))

    res = {"air_temperature" : air_temperature_latest, "air_humidity" : air_humidity_latest, "air_pressure" : air_pressure_latest, "soil_temperature" : soil_temperature_latest, "soil_humidity" : soil_humidity_latest}
    return res

if __name__ == '__main__':
    list_data = [ { "air_temperature": "26.5", "air_humidity": "50.9", "time": "1669790741610", "air_pressure": "101.12" }, { "air_temperature": "21.5", "air_humidity": "34.9", "time": "1669990729622", "air_pressure": "101.12" }, { "soil_humidity": "80.9", "time": "1669790697164", "soil_temperature": "24.5" }, { "soil_humidity": "56.9", "time": "1669990699154", "soil_temperature": "25.5" } ]
    res = get_latest_data(list_data)
    print(res)