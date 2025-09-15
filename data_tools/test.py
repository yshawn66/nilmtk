from nilmtk import DataSet, MeterGroup
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib import rcParams

# 设置matplotlib样式
plt.style.use('ggplot')
rcParams['figure.figsize'] = (13, 10)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 支持中文显示
plt.rcParams['axes.unicode_minus'] = False

# 加载数据集
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

print("=== NILMTK电表结构完整分析 ===")

# 1. 基本信息
print(f"数据集: {redd.metadata['name']}")
print(f"建筑物1电表总数: {len(elec.meters)}")

# 2. 主电表分析
mains = elec.mains()
print(f"\n=== 主电表信息 ===")
print(f"主电表数量: {len(mains.meters)}")
for meter in mains.meters:
    print(f"  - 主电表ID: {meter.instance}")
    # 检查可用的功率类型
    try:
        ac_types = meter.available_ac_types('power')
        print(f"    可用功率类型: {ac_types}")
    except:
        print(f"    无法获取功率类型信息")

# 3. 子电表分析
submeters = elec.submeters()
print(f"\n=== 子电表信息 ===")
print(f"子电表数量: {len(submeters.meters)}")

# 4. 嵌套电表组分析
nested = elec.nested_metergroups()
print(f"\n=== 嵌套电表组信息 ===")
print(f"嵌套组数量: {len(nested)}")
for i, group in enumerate(nested):
    if group.appliances:
        app_metadata = group.appliances[0].type
        app_type = app_metadata.get('type', 'unknown') if isinstance(app_metadata, dict) else str(app_metadata)
        meter_ids = [m.instance for m in group.meters]
        print(f"  组{i + 1}: {app_type}")
        print(f"    电表ID: {meter_ids}")
        print(f"    电表数量: {len(group.meters)}")

# 5. 设备统计和分类
device_stats = {}
print(f"\n=== 详细设备统计 ===")

for meter in elec.meters:
    meter_id = meter.instance

    if hasattr(meter, 'is_site_meter') and meter.is_site_meter():
        device_type = "主电表"
    elif meter.appliances:
        app_metadata = meter.appliances[0].type
        if isinstance(app_metadata, dict):
            device_type = app_metadata.get('type', 'unknown')
        else:
            device_type = str(app_metadata)
    else:
        device_type = "未知设备"

    if device_type not in device_stats:
        device_stats[device_type] = []
    device_stats[device_type].append(meter_id)

    print(f"  电表{meter_id}: {device_type}")

# 6. 设备类型汇总
print(f"\n=== 设备类型汇总 ===")
for device_type, meter_list in sorted(device_stats.items()):
    print(f"  {device_type}: {len(meter_list)}个 (电表ID: {meter_list})")

# 7. 能耗分析（如果数据可用）
print(f"\n=== 能耗分析 ===")
try:
    # 计算子电表能耗占比
    print("正在计算能耗占比...")
    proportion = elec.proportion_of_energy_submetered()
    print(f"子电表监测的能耗占比: {proportion:.2%}")
except Exception as e:
    print(f"无法计算能耗占比: {e}")

try:
    # 计算总能耗
    print("正在计算主电表总能耗...")
    total_energy = elec.mains().total_energy()
    print(f"主电表总能耗: {total_energy:.2f} kWh")
except Exception as e:
    print(f"无法计算总能耗: {e}")

try:
    # 计算各子电表能耗
    print("正在计算各子电表能耗...")
    energy_per_meter = elec.submeters().energy_per_meter()
    if not energy_per_meter.empty:
        print("各子电表能耗 (kWh):")
        # 只显示active功率的能耗
        if 'active' in energy_per_meter.index:
            active_energy = energy_per_meter.loc['active'].dropna()
            for meter_id, energy in active_energy.items():
                # 获取设备类型
                meter = elec[meter_id]
                if meter.appliances:
                    app_type = meter.appliances[0].type
                    if isinstance(app_type, dict):
                        device_name = app_type.get('type', f'电表{meter_id}')
                    else:
                        device_name = str(app_type)
                else:
                    device_name = f'电表{meter_id}'
                print(f"  {device_name} (电表{meter_id}): {energy:.2f} kWh")
except Exception as e:
    print(f"无法计算各子电表能耗: {e}")

# 8. 数据时间范围
try:
    timeframe = redd.get_timeframe()
    print(f"\n=== 数据时间信息 ===")
    print(f"时间范围: {timeframe}")
    print(f"开始时间: {timeframe.start}")
    print(f"结束时间: {timeframe.end}")
    duration = timeframe.end - timeframe.start
    print(f"数据持续时间: {duration.days}天")
except Exception as e:
    print(f"\n无法获取时间范围: {e}")

# 9. 可视化分析
print(f"\n=== 生成可视化图表 ===")

# 9.1 设备类型分布饼图
plt.figure(figsize=(12, 8))
device_counts = {k: len(v) for k, v in device_stats.items() if k != "主电表"}
if device_counts:
    plt.subplot(2, 2, 1)
    plt.pie(device_counts.values(), labels=device_counts.keys(), autopct='%1.1f%%')
    plt.title('设备类型分布')

# 9.2 电表数量柱状图
plt.subplot(2, 2, 2)
categories = list(device_counts.keys())
counts = list(device_counts.values())
plt.bar(categories, counts)
plt.title('各类设备数量')
plt.xticks(rotation=45)
plt.ylabel('数量')

# 9.3 尝试绘制能耗分布
try:
    energy_per_meter = elec.submeters().energy_per_meter()
    if not energy_per_meter.empty and 'active' in energy_per_meter.index:
        active_energy = energy_per_meter.loc['active'].dropna()

        plt.subplot(2, 2, 3)
        plt.bar(range(len(active_energy)), active_energy.values)
        plt.title('各电表能耗分布')
        plt.xlabel('电表ID')
        plt.ylabel('能耗 (kWh)')
        plt.xticks(range(len(active_energy)), active_energy.index)

        # 能耗占比饼图
        plt.subplot(2, 2, 4)
        # 获取设备标签
        labels = []
        for meter_id in active_energy.index:
            meter = elec[meter_id]
            if meter.appliances:
                app_type = meter.appliances[0].type
                if isinstance(app_type, dict):
                    label = app_type.get('type', f'电表{meter_id}')
                else:
                    label = str(app_type)
            else:
                label = f'电表{meter_id}'
            labels.append(f'{label}({meter_id})')

        plt.pie(active_energy.values, labels=labels, autopct='%1.1f%%')
        plt.title('能耗占比分布')

except Exception as e:
    print(f"无法生成能耗图表: {e}")

plt.tight_layout()
plt.savefig('nilmtk_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 10. 电表层次结构总结
print(f"\n=== 电表层次结构总结 ===")
print(f"总电表数: {len(elec.meters)}")
print(f"  ├─ 主电表: {len(mains.meters)}个")
print(f"  ├─ 嵌套组: {len(nested)}组 (包含{sum(len(g.meters) for g in nested)}个电表)")
print(f"  └─ 普通子电表: {len(submeters.meters) - sum(len(g.meters) for g in nested)}个")

# 11. 尝试获取功率数据样本
print(f"\n=== 功率数据样本 ===")
try:
    from nilmtk.timeframe import TimeFrame
    import datetime

    # 设置一个小的时间窗口
    start_time = datetime.datetime(2011, 4, 18, 0, 0, 0)
    end_time = datetime.datetime(2011, 4, 18, 1, 0, 0)  # 只取1小时数据
    timeframe = TimeFrame(start_time, end_time)

    print("尝试加载主电表功率数据...")
    main_power = next(mains.load(timeframe=timeframe))
    print(f"主电表功率数据形状: {main_power.shape}")
    print("前5行数据:")
    print(main_power.head())

except Exception as e:
    print(f"无法加载功率数据: {e}")

print(f"\n=== 分析完成 ===")
