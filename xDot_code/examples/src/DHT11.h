#ifndef __DHT11__
#define __DHT11__
#include "mbed.h"

/**  Example:
 * @code
 * #include "mbed.h"
 * #include "DHT11.h"
 *
 * DHT11 d;
 *
 * main()
 * {
 *     int s;
 *     s = d.readData();
 *     if (s != DHT11::OK) {
 *         printf("Error!\r\n");
 *     }
 *     else {
 *         printf("T:%d, H:%d\r\n", d.readTemperature(), d.readHumidity());
 *     }
 * }
 * @endcode
 */

class DHT11
{   
public:
    /** Create a DHT11 interface
     * @param pin 1-wire-like serial I/O port of DHT11
     */
    DHT11(PinName pin);
    ~DHT11();

    /** Reading the data from the DHT11
     * @return Error code
     *     0: OK.
     *     1: Reading the data too often.
     *     2: 1-wire bus is busy.
     *     3: DHT11 does not respond.
     *     4: DHT11 is not ready.
     *     5: Checksum is incorrect.
     *     6: Timeout.
     */
    int readData(void);

    /** Reading the humidity from the data
     * @return Humidity in %,
     * regardless of the error from readData()
     */
    int readHumidity(void);

    /** Reading the temperature from the data
     * @return Temperature in Celcius,
     * regardless of the error from readData()
     */
    int readTemperature(void);

    enum ErrorDHT11 {
        OK = 0,
        READ_TOO_OFTEN = 1,
        BUS_BUSY = 2,
        NOT_PRESENT = 3,
        NOT_READY = 4,
        CHKSUM_ERR = 5,
        WATCHDOG_ERR = 6,
    };

private:
    DigitalInOut io;
    InterruptIn io_irq;
    Timer t;
    uint32_t t_pulse_us;
    const static int t_tol_start;    
    const static int t_tol_pulse;
    bool first_time;
    uint64_t data;
    uint32_t chksum;
    uint32_t cnt;
    uint32_t wdt;
    bool eod;
    void init(void);
    void pos_edge(void);
    void neg_edge(void);
};

#endif