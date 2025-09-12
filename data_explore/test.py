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

# 选择时间段 - 修改这里的数字
start_idx = 0      # 开始索引
end_idx = 1000     # 结束索引

# 提取选定时间段数据
selected_data = data.iloc[start_idx:end_idx]

# 统计信息
print(f"数据点数: {len(selected_data)}")
print(f"功率范围: {selected_data.min().values[0]:.1f} - {selected_data.max().values[0]:.1f} W")
print(f"平均功率: {selected_data.mean().values[0]:.1f} W")

# 可视化
plt.figure(figsize=(10, 4))
plt.plot(selected_data.values)
plt.title(f'Power Consumption (索引 {start_idx}-{end_idx})')
plt.ylabel('Power (W)')
plt.show()
