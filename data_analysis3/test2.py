from nilmtk import DataSet
import matplotlib.pyplot as plt
import pandas as pd
from pandas.plotting import autocorrelation_plot
import os

# 加载数据集
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

# 1. 单日数据可视化
redd.set_window(start='2011-04-21', end='2011-04-22')
elec.plot()
plt.title("Plot sub-metered data for a single day")
plt.show()

# 2. 自相关图（使用少量数据）
print("正在绘制自相关图...")
redd.set_window(start='2011-04-21', end='2011-04-22')  # 只用1天数据
mains = elec.mains()

power_data = next(mains.load()).dropna()
# 采样减少数据量
if len(power_data) > 1000:
    power_data = power_data.iloc[::2]  # 每2个点取1个

autocorrelation_plot(power_data)
plt.title("Autocorrelation Plot")
plt.show()

#3 分析数据集中不同冰箱设备的能耗模式和差异 还有点小问题

# 4. 设备相关性分析 哪几个设备会同时启用 皮尔森系数
print("正在计算设备相关性...")
redd.set_window(start='2011-04-18', end='2011-04-25')  # 使用一周数据
correlation_df = elec.pairwise_correlation()
print("Correlation dataframe of the appliances:")
print(correlation_df)

print("完成！")
