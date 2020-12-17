from datetime import datetime as dt
# 文字列
time_str = '2020-09-12 12:22:30+09:00'
# timezoneを含んだdatetime型
time_dt = dt.fromisoformat(time_str)

print(time_dt)
print(time_dt.tzinfo)
