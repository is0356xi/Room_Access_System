from scd30_i2c import SCD30
import time


class Scd_30:
    def __init__(self):
        self.scd30 = SCD30()

        self.scd30.set_measurement_interval(2)
        self.scd30.start_periodic_measurement()

        time.sleep(1)


    def get_value(self):
        while True:
            if self.scd30.get_data_ready():
                m = self.scd30.read_measurement()
                if m is not None:
                    values = {}
                    values["CO2"] = round(m[0],2)
                    values["temp"] = round(m[1],2)
                    values["rh"] = round(m[2],2)
                    
                    return values
                else:
                    time.sleep(0.2)

    def main(self):
        while True:
            if self.scd30.get_data_ready():
                m = self.scd30.read_measurement()
                if m is not None:
                    print(f"CO2: {m[0]:.2f}ppm, temp: {m[1]:.2f}'C, rh: {m[2]:.2f}%")
                    time.sleep(2)
                else:
                    time.sleep(0.2)

if __name__ == "__main__":
    scd30 = Scd_30()
    # scd30.main()

    value = scd30.get_value()
    print(value)