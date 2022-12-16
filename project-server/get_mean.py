def get_mean_data(list_data):
    air_temperature_total = 0.0
    air_humidity_total = 0.0
    air_pressure_total = 0.0
    soil_humidity_total = 0.0
    soil_temperature_total = 0.0
    air_sensor_count = 0
    soil_sensor_count = 0

    for sensor_data in list_data:
        if sensor_data.get("air_temperature") is not None:
            air_temperature_total += float(sensor_data.get("air_temperature"))
            air_humidity_total += float(sensor_data.get("air_humidity"))
            air_pressure_total += float(sensor_data.get("air_pressure"))
            air_sensor_count += 1
        else:
            soil_temperature_total += float(sensor_data.get("soil_temperature"))
            soil_humidity_total += float(sensor_data.get("soil_humidity"))
            soil_sensor_count += 1
    
    air_temperature_mean = air_temperature_total / air_sensor_count
    air_humidity_mean = air_humidity_total / air_sensor_count
    air_pressure_mean = air_pressure_total / air_sensor_count

    soil_temperature_mean = soil_temperature_total / soil_sensor_count
    soil_humidity_mean = soil_humidity_total / soil_sensor_count

    res = {"air_temperature_mean" : air_temperature_mean, "air_humidity_mean" : air_humidity_mean, "air_pressure_mean" : air_pressure_mean, "soil_temperature_mean" : soil_temperature_mean, "soil_humidity_mean" : soil_humidity_mean}
    return res

if __name__ == '__main__':
    list_data = [ { "air_temperature": "26.5", "air_humidity": "50.9", "time": "1669790741610", "air_pressure": "101.12" }, { "air_temperature": "24.5", "air_humidity": "51.9", "time": "1669790729622", "air_pressure": "101.12" }, { "soil_humidity": "80.9", "time": "1669790697164", "soil_temperature": "24.5" }, { "soil_humidity": "78.9", "time": "1669790699154", "soil_temperature": "23.5" }, { "air_temperature": "23.7", "air_humidity": "42.9", "time": "1669790716162", "air_pressure": "101.12" }, { "air_temperature": "24.5", "air_humidity": "46.9", "time": "1669790743740", "air_pressure": "101.12" }, { "air_temperature": "25.5", "air_humidity": "42.9", "time": "1669790702937", "air_pressure": "101.12" }, { "air_temperature": "26.5", "air_humidity": "50.9", "time": "1669790728329", "air_pressure": "101.12" }, { "soil_humidity": "80.4", "time": "1669790712389", "soil_temperature": "23.5" }, { "soil_humidity": "80.9", "time": "1669790710269", "soil_temperature": "22.8" }, { "air_temperature": "26.5", "air_humidity": "50.9", "time": "1669790688676", "air_pressure": "101.12" }, { "soil_humidity": "80.9", "time": "1669790724577", "soil_temperature": "22.5" }, { "soil_humidity": "80.9", "time": "1669790737815", "soil_temperature": "22.5" } ]
    get_mean_data(list_data)