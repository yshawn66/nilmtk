# 查看每个电表记录的设备信息 - 最简版
import os
from nilmtk import DataSet
import warnings

warnings.filterwarnings('ignore')

# 动态路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')

redd = DataSet(data_path)
building1 = redd.buildings[1]

print("=== 电表设备信息 ===")
for i, meter in enumerate(building1.elec.meters):
    # 获取设备名称
    appliance = meter.appliances
    if appliance:
        device_name = list(appliance)[0].metadata['type']
        print(f"电表 {i}: {device_name}")
    else:
        print(f"电表 {i}: 主电表 (总功率)")

print("完成!")
