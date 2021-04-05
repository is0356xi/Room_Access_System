import smbus
import time
from numpy.random import *


def swap16(x):
    return (((x << 8) & 0xFF00) |
        ((x >> 8) & 0x00FF))

def sign16(x):
    return ( -(x & 0b1000000000000000) |
        (x & 0b0111111111111111) )

def sign8(x):
    return ( -(x & 0b10000000) | (x & 0b01111111) )

def test():
    i2c = smbus.SMBus(1)
    addr=0x68
    Vref=2.048

    for i in range(50):
        # i2c.write_byte(addr, 0b10001000)
        # i2c.write_byte(addr, 0b10011000)
        i2c.write_byte(addr, 0b10101000)
        # i2c.write_byte(addr, 0b10111000)
        # i2c.write_byte(addr, 0b11001000)
        # i2c.write_byte(addr, 0b11011000)
        # i2c.write_byte(addr, 0b11101000)
        # i2c.write_byte(addr, 0b11111000)
        time.sleep(0.3)
        # data1 = i2c.read_word_data(addr,0x00)
        # raw1 = swap16(int(hex(data1),16))

        data2 = i2c.read_i2c_block_data(addr,0x00)
        raw2 = (data2[1] << 8 | data2[0])
        print(data2, hex(raw2))

def main():
    i2c = smbus.SMBus(1)
    addr=0x68
    Vref=2.048

    data1 = []
    data2 = []

    for i in range(200):
    #i2c.write_byte(addr, 0b10011000) #16bit
        i2c.write_byte(addr, 0b10001000) #16bit
        time.sleep(0.5)

        block_data = i2c.read_i2c_block_data(addr,0x00, 2)
        raw = (block_data[0] << 8 | block_data[1])
        volts1 = round((Vref * int(hex(raw),16) / 32767),5)

        print(block_data, hex(raw), volts1)

        # data = i2c.read_word_data(addr,0x00)
        # raw = swap16(int(hex(data),16))
        # raw_s = sign16(int(hex(raw),16))
        # volts1 = round((Vref * raw_s / 32767),5)

        # print(block_data, data, raw, raw_s, volts1)
        



        # i2c.write_byte(addr, 0b10111000) #16bit
        # time.sleep(0.1)

            
        

        # data = i2c.read_word_data(addr,0x00)
        # raw = swap16(int(hex(data),16))
        # raw_s = sign16(int(hex(raw),16))
        # volts2 = round((Vref * raw_s / 32767),5)

        # print(hex(data), int(hex(data), 16),swap16(int(hex(data),16)),volts2)

        # i2c.write_byte(addr, 0b11011000) #16bit
        # time.sleep(0.2)

        # data = i2c.read_word_data(addr,0x00)
        # raw = swap16(int(hex(data),16))
        # raw_s = sign16(int(hex(raw),16))
        # volts3 = round((Vref * raw_s / 32767),5)

        

        # i2c.write_byte(addr, 0b11111000) #16bit
        # time.sleep(0.2)

        # data = i2c.read_word_data(addr,0x00)
        # raw = swap16(int(hex(data),16))
        # raw_s = sign16(int(hex(raw),16))
        # volts4 = round((Vref * raw_s / 32767),5)

        #print ("ch1=" + str(volts1) +"V")
        #print ("ch2=" + str(volts2) +"V")
        #print ("ch3=" + str(volts3) +"V")
        #print ("ch4=" + str(volts4) +"V")
        #print ("ch1-4=" + str(volts1) +"V "+ str(volts2) +"V "+ str(volts3) +"V " + str(volts4) +"V ")
        #print (str(volts1))

        # out_msg = r'{'
        # out_msg += r'"ch1":'
        # out_msg += str(volts1)
        # out_msg += r','
        # out_msg += r'"ch2":'
        # out_msg += str(volts2)
        # out_msg += r','
        # out_msg += r'"ch3":'
        # out_msg += str(volts3)
        # out_msg += r','
        # out_msg += r'"ch4":'
        # out_msg += str(volts4)
        # out_msg += r'}'
        # print(out_msg)

        # data1.append(volts1)
        # data2.append(volts2)

        print()
        

        # time.sleep(1)
    
    # show(data1, data2)


def show(data1, data2):
    import matplotlib.pyplot as plt

    plt.figure()
    plt.plot(range(len(data1)), data1, color="blue", linestyle="-", label="odor")
    plt.plot(range(len(data2)), data2, color="green", linestyle="--", label="sound")
    plt.legend()
    plt.xlabel('time')
    plt.ylabel("value")
    plt.title("sensor value")
    plt.grid()

    plt.show()



if __name__ == "__main__":
    main()
    # test()