from nilmtk import DataSet
import os

# 加载数据集
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')
iawe = DataSet(data_path)
fridge = iawe.buildings[1].elec['fridge']

# 1. 加载无功功率数据
reactive_power = next(fridge.load(physical_quantity='power', ac_type='reactive'))
print("无功功率数据:")
print(reactive_power.head())

# 2. 加载电压数据
voltage_data = next(fridge.load(physical_quantity='voltage'))
print("\n电压数据:")
print(voltage_data.head())

# 3. 加载所有功率数据
all_power = next(fridge.load(physical_quantity='power'))
print("\n所有功率数据:")
print(all_power.head())

#相比于2 只加载需要的数据，节省内存；2需要加载所有数据，然后手动选择列