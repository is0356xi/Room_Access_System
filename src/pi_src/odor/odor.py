import smbus
import time

def get_odor_value():
    i2c = smbus.SMBus(1)
    addr=0x68
    Vref=2.048

    i2c.write_byte(addr, 0b10001000) #16bit
    time.sleep(0.5)

    block_data = i2c.read_i2c_block_data(addr,0x00, 2)
    raw = (block_data[0] << 8 | block_data[1])
    volts1 = round((Vref * int(hex(raw),16) / 32767),5)

    return volts1

def main():
    measure_num = 5  #計測回数
    odor_sum = 0

    for i in range(measure_num):
        volts1 = get_odor_value()
        odor_sum += volts1

    odor_avg = odor_sum/measure_num

    print(round(odor_avg,4))

if __name__ == "__main__":
    main()
    # test()