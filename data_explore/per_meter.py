# 查看电表信息 + 单个电表数据
import os
from nilmtk import DataSet
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')
redd = DataSet(data_path)
building1 = redd.buildings[1]

# 显示所有电表
print("=== 电表列表 ===")
for i, meter in enumerate(building1.elec.meters):
    appliance = meter.appliances
    name = list(appliance)[0].metadata['type'] if appliance else "主电表"
    print(f"电表 {i}: {name}")

# 查看指定电表数据
meter_index = 3  # 📝 修改这里选择电表
meter = building1.elec.meters[meter_index]
data = next(meter.load())

print(f"\n📊 电表 {meter_index} 数据:")
print(f"数据点: {len(data)}")
print(f"时间范围: {data.index[0]} 到 {data.index[-1]}")
print(f"功率: {data.min().values[0]:.1f} - {data.max().values[0]:.1f} W")

# 📅 选择日期范围 (可选)
start_date = '2013-07-13'  # 📝 修改日期
end_date = '2013-07-14'

filtered_data = data[start_date:end_date]
if len(filtered_data) > 0:
    print(f"选择日期数据点: {len(filtered_data)}")
    plt.plot(filtered_data.values)
    plt.title(f'电表 {meter_index} ({start_date})')
else:
    plt.plot(data[:1000].values)
    plt.title(f'电表 {meter_index} (前1000点)')

plt.show()
