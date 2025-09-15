from nilmtk import DataSet
import os

# 加载数据集
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')
iawe = DataSet(data_path)
fridge = iawe.buildings[1].elec['fridge']

# 1. 指定AC类型加载（有功功率）
active_power = next(fridge.load(ac_type='active'))
print("有功功率数据（原始频率）:")
print(active_power.head())
print(f"数据形状: {active_power.shape}")

# 2. 重采样到指定周期（60秒间隔）
resampled_data = next(fridge.load(ac_type='active', sample_period=60))
print("\n重采样数据（60秒间隔）:")
print(resampled_data.head())
print(f"数据形状: {resampled_data.shape}")

# 3. 对比不同采样周期
print("\n不同采样周期对比:")
for period in [30, 60, 300]:  # 30秒、1分钟、5分钟
    data = next(fridge.load(ac_type='active', sample_period=period))
    print(f"{period}秒采样 - 数据点数: {len(data)}")
