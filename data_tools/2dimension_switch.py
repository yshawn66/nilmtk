from nilmtk import DataSet
import os

# 修正文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')

# 检查文件是否存在
if not os.path.exists(data_path):
    print(f"文件不存在: {data_path}")
    print(f"当前目录: {current_dir}")
    exit()

# 加载数据集
iawe = DataSet(data_path)
fridge = iawe.buildings[1].elec['fridge']

# 加载所有列数据
all_data = next(fridge.load())
print("所有参数数据:")
print(all_data.head())

# 加载单列功率数据
power_data = next(fridge.power_series())
print("\n有功功率数据:")
print(power_data.head())

# 加载无功功率数据
reactive_power = next(fridge.power_series(ac_type='reactive'))
print("\n无功功率数据:")
print(reactive_power.head())
