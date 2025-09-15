from nilmtk import DataSet
import matplotlib.pyplot as plt
import os

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

# 1. 能耗占比饼图
print("=== 1. 能耗占比分析 ===")
fraction = elec.submeters().fraction_per_meter().dropna()
labels = elec.get_labels(fraction.index)
plt.figure(figsize=(10, 10))
fraction.plot(kind='pie', labels=labels)
plt.title('Energy Consumption by Appliance')
plt.ylabel('')
plt.show()

# 2. 电路连接图
print("\n=== 2. 电路连接图 ===")
elec.draw_wiring_graph()

# 3. 设备使用时间图
print("\n=== 3. 设备使用时间模式 ===")
plt.figure(figsize=(15, 8))
downstream_meters = elec.meters_directly_downstream_of_mains()
downstream_meters.plot_when_on(on_power_threshold=40)
plt.title('Appliance Usage Patterns')
plt.show()

print("直接连接到主电表的设备：")
print(downstream_meters)

# 4. 单个设备分析（以冰箱为例）
print("\n=== 4. 单个设备详细分析（冰箱） ===")
fridge_meter = elec['fridge']

# 4.1 获取上游电表
print("冰箱的上游电表：")
upstream = fridge_meter.upstream_meter()
print(upstream)

# 4.2 设备元数据
print("\n冰箱电表的设备信息：")
device_info = fridge_meter.device
for key, value in device_info.items():
    print(f"{key}: {value}")

# 4.3 主要电器
print(f"\n主要电器: {fridge_meter.dominant_appliance()}")

# 4.4 总能耗
print(f"\n冰箱总能耗: {fridge_meter.total_energy()} kWh")

# 4.5 冰箱功率时间序列图
print("\n=== 5. 冰箱功率时间序列 ===")
plt.figure(figsize=(15, 8))
fridge_meter.plot()
plt.title('Fridge Power Consumption Over Time')
plt.ylabel('Power (W)')
plt.show()

print("\n分析完成！")
