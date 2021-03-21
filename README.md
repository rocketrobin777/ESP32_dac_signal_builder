# ESP32_dac_signal_builder
Python Script and C++/.ino-Project for ESP32 to use predefined signal with dma

Signal builder in Python with preview and own fft routine.
Signal.h is generated depending on own signal with uint8_t buf[N] as dma variable.
The dac, based on dma does not need any cpu power and works independent.
N >= 512 is recommended.
max(yd) <= 255, because dac has only 8 bit
