/*
 Name:		DAC_Test.ino
 Created:	2021/03/21
 Author:	robin
*/
#include "driver/dac.h"
#include "driver/i2s.h"
#include "Signal.h"

i2s_config_t i2s_config = {
     .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX | I2S_MODE_DAC_BUILT_IN), //mode
     .sample_rate = 100000, //sample rate
     .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT, // DAC uses only 8 Bit of MSB
     .channel_format = I2S_CHANNEL_FMT_RIGHT_LEFT, // channel ESP32
     .communication_format = (i2s_comm_format_t)I2S_COMM_FORMAT_I2S_MSB, //format for I2S
     .intr_alloc_flags = 0, // standard interrupt 
     .dma_buf_count = 2, //number of FIFO buffer
     .dma_buf_len = 32, //siue of FIFO buffer
     .use_apll = 0 //PLL synch
};

void setFrequency(double frequency) {
	int size = sizeof(buf)/8;
    uint32_t rate = 2*frequency*size; // calc sample rate 
    i2s_driver_uninstall((i2s_port_t)0); // kill I2S driver
    i2s_config.sample_rate = rate; // edit config 
    i2s_config.dma_buf_len = size; // dma length
    i2s_driver_install((i2s_port_t)0, &i2s_config, 0, NULL); // update config
    i2s_set_sample_rates((i2s_port_t)0, rate);
    i2s_write_bytes((i2s_port_t)0, (const char*)&buf, size * 8, 100);
    i2s_set_pin((i2s_port_t)0, NULL);
    dac_i2s_enable();
}
void setup() {
	Serial.begin(115200);
  Serial.print("size of signal: ");
  Serial.println(sizeof(buf));
  setFrequency(50);
}
void loop() {
  
}
