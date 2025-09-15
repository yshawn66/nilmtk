from nilmtk import DataSet
import os
import pandas as pd

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

# 1. 能源子计量比例
print("=== 能源子计量比例 ===")
proportion = elec.proportion_of_energy_submetered()
print(f"子计量比例: {proportion}")

# 2. 查看主电表和子电表的功率类型
print("\n=== 功率类型 ===")
mains = elec.mains()
print(f"主电表功率类型: {mains.available_ac_types('power')}")
print(f"子电表功率类型: {elec.submeters().available_ac_types('power')}")

# 3. 加载数据样本 - 修复版本
print("\n=== 数据样本 ===")
try:
    # 方法1：直接从主电表加载数据
    mains_data = next(elec.mains().load())
    print("主电表数据样本:")
    print(mains_data.head(10))
except Exception as e:
    print(f"加载主电表数据出错: {e}")

    # 方法2：从子电表加载数据
    try:
        submeter_data = next(elec.submeters().load())
        print("子电表数据样本:")
        print(submeter_data.head(10))
    except Exception as e:
        print(f"加载子电表数据也出错: {e}")

        # 方法3：直接从特定电表加载
        try:
            specific_meter = elec[2]  # 选择电表2
            specific_data = next(specific_meter.load())
            print("特定电表数据样本:")
            print(specific_data.head(10))
        except Exception as e:
            print(f"所有数据加载方法都失败: {e}")

# 4. 总能耗
print("\n=== 总能耗 ===")
try:
    total_energy = elec.mains().total_energy()
    print(f"总能耗: {total_energy}")
except Exception as e:
    print(f"计算总能耗出错: {e}")

# 5. 各子电表能耗
print("\n=== 各子电表能耗 ===")
try:
    energy_per_meter = elec.submeters().energy_per_meter()
    print(energy_per_meter)

    # 6. 筛选高能耗电表（>20kWh）
    print("\n=== 高能耗电表 (>20kWh) ===")
    if 'active' in energy_per_meter.index:
        active_energy = energy_per_meter.loc['active']
        high_energy = active_energy[active_energy > 20]
        print(high_energy)
    else:
        print("未找到active功率数据")

    # 7. 能耗比例
    print("\n=== 各电表能耗比例 ===")
    fraction = elec.submeters().fraction_per_meter().dropna()
    if 'active' in fraction.index:
        print(fraction.loc['active'])
    else:
        print("未找到active功率比例数据")

except Exception as e:
    print(f"计算子电表能耗出错: {e}")

print("\n程序执行完成！")
