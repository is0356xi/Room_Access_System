import odor
import scd30

od = odor.Odor()
scd = scd30.Scd_30()

# 辞書型で{CO2, temp, rh}を取得
values = scd.get_value()

# 臭気センサの値odorを辞書に追加
odor_val = od.get_value()
values["odor"] = odor_val


print(values)