# IAWE数据集基本信息
import os
from nilmtk import DataSet
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 动态路径
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')

print(f"数据路径: {data_path}")
print("正在加载数据...")

iawe = DataSet(data_path)
print(f"IAWE数据集包含建筑物数量: {len(iawe.buildings)}")

building1 = iawe.buildings[1]

# 选中建筑物信息
print(f"选择建筑物1，其电表数量: {len(building1.elec.meters)}")

# 获取主电表数据
main_meter = building1.elec.mains().meters[1]
data = next(main_meter.load())

# 数据统计
print(f"数据点数: {len(data)}")
print(f"时间范围: {data.index[0]} 到 {data.index[-1]}")  # 新增时间范围
print(f"数据时长: {data.index[-1] - data.index[0]}")    # 新增数据时长
print(f"功率范围: {data.min().values[0]:.1f} - {data.max().values[0]:.1f} W")
print(f"平均功率: {data.mean().values[0]:.1f} W")

# 简单可视化
sample = data[:1000]  # 前1000个点
plt.figure(figsize=(10, 4))
plt.plot(sample.values)
plt.title('IAWE Power Consumption')
plt.ylabel('Power (W)')
plt.show()

print("完成!")
