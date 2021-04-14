import smbus
import time

class Odor:
    def __init__(self):

        self.i2c = smbus.SMBus(1)
        self.addr = 0x68
        self.Vref = 2.048


    def get_odor_value(self):
        self.i2c.write_byte(self.addr, 0b10001000) #16bit
        time.sleep(0.5)

        block_data = self.i2c.read_i2c_block_data(self.addr,0x00, 2)
        raw = (block_data[0] << 8 | block_data[1])
        volts1 = round((self.Vref * int(hex(raw),16) / 32767),5)

        return volts1


    def get_value(self):
        measure_num = 5  #計測回数
        odor_sum = 0

        for i in range(measure_num):
            volts1 = self.get_odor_value()
            odor_sum += volts1

        odor_avg = odor_sum/measure_num

        return (round(odor_avg,3))


    def main(self):
        measure_num = 5  #計測回数
        odor_sum = 0

        for i in range(measure_num):
            volts1 = self.get_odor_value()
            odor_sum += volts1

        odor_avg = odor_sum/measure_num

        print(round(odor_avg,3))

if __name__ == "__main__":
    odor = Odor()
    # odor.main()
    
    value = odor.get_value()
    print(value)