# redd数据集时间段分析 - 简化版
import os
from nilmtk import DataSet
import matplotlib.pyplot as plt
import warnings

warnings.filterwarnings('ignore')

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')

redd = DataSet(data_path)
building1 = redd.buildings[1]
main_meter = building1.elec.mains().meters[0]
data = next(main_meter.load())

# 选择时间段 - 修改这里的日期时间
start_time = '2011-04-18 10:00'  # 开始时间
end_time = '2011-04-18 12:00'    # 结束时间

# 提取选定时间段数据
selected_data = data[start_time:end_time]

# 统计信息
print(f"数据点数: {len(selected_data)}")
print(f"功率范围: {selected_data.min().values[0]:.1f} - {selected_data.max().values[0]:.1f} W")
print(f"平均功率: {selected_data.mean().values[0]:.1f} W")

# 可视化
plt.figure(figsize=(10, 4))
plt.plot(selected_data.values)
plt.title(f'Power Consumption ({start_time} 到 {end_time})')
plt.ylabel('Power (W)')
plt.show()
