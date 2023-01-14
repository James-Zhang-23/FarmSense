#include "dot_util.h"
#include "RadioEvent.h"
#include "BME280.h"
#include "DHT11.h"

#if ACTIVE_EXAMPLE == OTA_EXAMPLE

/////////////////////////////////////////////////////////////////////////////
// -------------------- DOT LIBRARY REQUIRED ------------------------------//
// * Because these example programs can be used for both mDot and xDot     //
//     devices, the LoRa stack is not included. The libmDot library should //
//     be imported if building for mDot devices. The libxDot library       //
//     should be imported if building for xDot devices.                    //
// * https://developer.mbed.org/teams/MultiTech/code/libmDot-dev-mbed5/    //
// * https://developer.mbed.org/teams/MultiTech/code/libmDot-mbed5/        //
// * https://developer.mbed.org/teams/MultiTech/code/libxDot-dev-mbed5/    //
// * https://developer.mbed.org/teams/MultiTech/code/libxDot-mbed5/        //
/////////////////////////////////////////////////////////////////////////////


/////////////////////////////////////////////////////////////
// * these options must match the settings on your gateway //
// * edit their values to match your configuration         //
// * frequency sub band is only relevant for the 915 bands //
// * either the network name and passphrase can be used or //
//     the network ID (8 bytes) and KEY (16 bytes)         //
/////////////////////////////////////////////////////////////
static std::string network_name = "antisleep";
static std::string network_passphrase = "antisleep";
static uint8_t network_id[] = { 0x6C, 0x4E, 0xEF, 0x66, 0xF4, 0x79, 0x86, 0xA6 };
static uint8_t network_key[] = { 0x1F, 0x33, 0xA1, 0x70, 0xA5, 0xF1, 0xFD, 0xA0, 0xAB, 0x69, 0x7A, 0xAE, 0x2B, 0x95, 0x91, 0x6B };
static uint8_t frequency_sub_band = 7;
static lora::NetworkType network_type = lora::PUBLIC_LORAWAN;
static uint8_t join_delay = 5;
static uint8_t ack = 0;
static bool adr = true;

// deepsleep consumes slightly less current than sleep
// in sleep mode, IO state is maintained, RAM is retained, and application will resume after waking up
// in deepsleep mode, IOs float, RAM is lost, and application will start from beginning after waking up
// if deep_sleep == true, device will enter deepsleep mode
static bool deep_sleep = false;
// AnalogIn soil_moisture(PB_0);
// Dht11 sensor(PB_0);
DHT sensor(PB_2, DHT11);
mDot* dot = NULL;
lora::ChannelPlan* plan = NULL;

mbed::UnbufferedSerial pc(USBTX, USBRX);

#if defined(TARGET_XDOT_L151CC)
I2C i2c(I2C_SDA, I2C_SCL);

ISL29011 lux(i2c);
// BME280 sensor(I2C_SDA, I2C_SCL);
#else
AnalogIn lux(XBEE_AD0);
#endif

float ReadAirTemperature() {
  int var1, var2;
  char temp_data[4];
  char ack[1] = {1};

  int adc_T = 0;
  unsigned int dig_T1 = 0;
  int dig_T2 = 0;
  int dig_T3 = 0;

//   i2c.write(0xFA, ack, 1);
  i2c.read(0xFA, temp_data, 3);
  adc_T = ((unsigned int)temp_data[0] << 16) + ((unsigned int)temp_data[1] << 8) + ((unsigned int)temp_data[2] << 0);
//   i2c.write(0x88, ack, 1);
  i2c.read(0x88, temp_data, 2);
  dig_T1 = ((unsigned int)temp_data[1] << 8) + ((unsigned int)temp_data[0] << 0);
//   i2c.write(0x8A, ack, 1);
  i2c.read(0x8A, temp_data, 2);
  dig_T2 = ((unsigned int)temp_data[1] << 8) + ((unsigned int)temp_data[0] << 0);
//   i2c.write(0x8C, ack, 1);
  i2c.read(0x8C, temp_data, 2);
  dig_T3 = ((unsigned int)temp_data[1] << 8) + ((unsigned int)temp_data[0] << 0);

  if (adc_T == 0x800000) // value in case temp measurement was disabled
    return 0.0;
  adc_T >>= 4;

  var1 = (int)((adc_T / 8) - (dig_T1 * 2));
  var1 = (var1 * ((int)dig_T2)) / 2048;
  var2 = (int)((adc_T / 16) - (dig_T1));
  var2 = (((var2 * var2) / 4096) * ((int)dig_T3)) / 16384;

  int t_fine = var1 + var2;

  int T = (t_fine * 5 + 128) / 256;

  return (float)T / 100;
}


float ReadSoilTemperature() {
    char buf[4] = {1, 0, 0, 0};
    i2c.write(0x36, buf, 1);
    i2c.read(0x36, buf, 4);
    int32_t ret = ((uint32_t)buf[0] << 24) | ((uint32_t)buf[1] << 16) |
                    ((uint32_t)buf[2] << 8) | (uint32_t)buf[3];
    return (1.0 / (1UL << 16)) * ret;
}

int main() {
    // Custom event handler for automatically displaying RX data
    RadioEvent events;

    pc.baud(115200);

#if defined(TARGET_XDOT_L151CC)
    i2c.frequency(400000);
#endif

    mts::MTSLog::setLogLevel(mts::MTSLog::TRACE_LEVEL);

    // Create channel plan
    plan = create_channel_plan();
    assert(plan);

    dot = mDot::getInstance(plan);
    assert(dot);

    // attach the custom events handler
    dot->setEvents(&events);

    if (!dot->getStandbyFlag() && !dot->getPreserveSession()) {
        logInfo("mbed-os library version: %d.%d.%d", MBED_MAJOR_VERSION, MBED_MINOR_VERSION, MBED_PATCH_VERSION);

        // start from a well-known state
        logInfo("defaulting Dot configuration");
        dot->resetConfig();
        dot->resetNetworkSession();

        // make sure library logging is turned on
        dot->setLogLevel(mts::MTSLog::INFO_LEVEL);

        // update configuration if necessary
        if (dot->getJoinMode() != mDot::OTA) {
            logInfo("changing network join mode to OTA");
            if (dot->setJoinMode(mDot::OTA) != mDot::MDOT_OK) {
                logError("failed to set network join mode to OTA");
            }
        }

        // To preserve session over power-off or reset enable this flag
        // dot->setPreserveSession(true);

        // in OTA and AUTO_OTA join modes, the credentials can be passed to the library as a name and passphrase or an ID and KEY
        // only one method or the other should be used!
        // network ID = crc64(network name)
        // network KEY = cmac(network passphrase)
        update_ota_config_name_phrase(network_name, network_passphrase, frequency_sub_band, network_type, ack);
        //update_ota_config_id_key(network_id, network_key, frequency_sub_band, network_type, ack);

        // configure network link checks
        // network link checks are a good alternative to requiring the gateway to ACK every packet and should allow a single gateway to handle more Dots
        // check the link every count packets
        // declare the Dot disconnected after threshold failed link checks
        // for count = 3 and threshold = 5, the Dot will ask for a link check response every 5 packets and will consider the connection lost if it fails to receive 3 responses in a row
        update_network_link_check_config(3, 5);

        // enable or disable Adaptive Data Rate
        dot->setAdr(adr);

        // Configure the join delay
        dot->setJoinDelay(join_delay);

        // save changes to configuration
        logInfo("saving configuration");
        if (!dot->saveConfig()) {
            logError("failed to save configuration");
        }

        // display configuration
        display_config();
    } else {
        // restore the saved session if the dot woke from deepsleep mode
        // useful to use with deepsleep because session info is otherwise lost when the dot enters deepsleep
        logInfo("restoring network session from NVM");
        dot->restoreNetworkSession();
    }

    int raw_data = 0;
    char out_humidity[5];
    char out_temperature[6];
    char out_pressure[8];
    
    char bm_reset = 0xB6;
    i2c.write(0xE0, &bm_reset, 1);
    while (true) {
        
        // ThisThread::sleep_for(5000ms);
        uint16_t light;
        std::vector<uint8_t> tx_data;

        // join network if not joined
        if (!dot->getNetworkJoinStatus()) {
            join_network();
        }

        // raw_data = sensor.read_u16();

// --------------------------------------------------------
        int res = sensor.readData();
        if (res == ERROR_NONE) {
            float humi = sensor.ReadHumidity();
            snprintf(out_humidity, 5, "%f", humi);
            float tempc = sensor.ReadTemperature(CELCIUS);
            snprintf(out_temperature, 6, "%f", tempc);
            float air_pressure = sensor.Readpressure();
            snprintf(out_pressure, 8, "%f", air_pressure);
        }

        tx_data.push_back('[');
        for (int i = 0; i < sizeof(out_humidity); ++i) {
            tx_data.push_back(out_humidity[i]);
        }
        tx_data.push_back(',');
        for (int i = 0; i < sizeof(out_temperature); ++i) {
            tx_data.push_back(out_temperature[i]);
        }
        tx_data.push_back(',');
        for (int i = 0; i < sizeof(out_pressure); ++i) {
            tx_data.push_back(out_pressure[i]);
        }
        tx_data.push_back(']');

// --------------------------------------------------------
        send_data(tx_data);

#if defined(TARGET_XDOT_L151CC)
        // // configure the ISL29011 sensor on the xDot-DK for continuous ambient light sampling, 16 bit conversion, and maximum range
        // lux.setMode(ISL29011::ALS_CONT);
        // lux.setResolution(ISL29011::ADC_16BIT);
        // lux.setRange(ISL29011::RNG_64000);

        // // get the latest light sample and send it to the gateway
        // light = lux.getData();
        // tx_data.push_back((light >> 8) & 0xFF);
        // tx_data.push_back(light & 0xFF);
        // logInfo("light: %lu [0x%04X]", light, light);
        // send_data(tx_data);

        // // put the LSL29011 ambient light sensor into a low power state
        // lux.setMode(ISL29011::PWR_DOWN);
#else
        // get some dummy data and send it to the gateway
        light = lux.read_u16();
        tx_data.push_back((light >> 8) & 0xFF);
        tx_data.push_back(light & 0xFF);
        logInfo("light: %lu [0x%04X]", light, light);
        send_data(tx_data);
#endif

        // if going into deepsleep mode, save the session so we don't need to join again after waking up
        // not necessary if going into sleep mode since RAM is retained
        if (deep_sleep) {
            logInfo("saving network session to NVM");
            dot->saveNetworkSession();
        }

        // ONLY ONE of the three functions below should be uncommented depending on the desired wakeup method
        //sleep_wake_rtc_only(deep_sleep);
        //sleep_wake_interrupt_only(deep_sleep);
        sleep_wake_rtc_or_interrupt(deep_sleep);
    }

    return 0;
}

#endif
