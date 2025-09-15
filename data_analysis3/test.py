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
    # 修复：正确获取电表ID
    meter_id = meter.instance
    print(f"  - 主电表ID: {meter_id}")
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
        # 修复：正确获取电表ID列表
        meter_ids = [m.instance for m in group.meters]
        print(f"  组{i + 1}: {app_type}")
        print(f"    电表ID: {meter_ids}")
        print(f"    电表数量: {len(group.meters)}")

# 5. 设备统计和分类
device_stats = {}
print(f"\n=== 详细设备统计 ===")

for meter in elec.meters:
    # 修复：正确获取电表ID
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
    # 计算总能耗 - 修复格式化问题
    print("正在计算主电表总能耗...")
    total_energy = elec.mains().total_energy()
    # 处理Series或其他数据类型
    if hasattr(total_energy, 'values'):
        total_energy_value = total_energy.values[0] if len(total_energy.values) > 0 else total_energy
    else:
        total_energy_value = float(total_energy)
    print(f"主电表总能耗: {total_energy_value:.2f} kWh")
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
                if hasattr(meter_id, 'instance'):
                    # 处理单个电表
                    actual_id = meter_id.instance
                    meter = elec[actual_id]
                    if meter.appliances:
                        app_type = meter.appliances[0].type
                        if isinstance(app_type, dict):
                            device_name = app_type.get('type', f'电表{actual_id}')
                        else:
                            device_name = str(app_type)
                    else:
                        device_name = f'电表{actual_id}'
                    print(f"  {device_name} (电表{actual_id}): {energy:.2f} kWh")
                else:
                    # 处理电表组
                    print(f"  电表组 {meter_id}: {energy:.2f} kWh")
except Exception as e:
    print(f"无法计算各子电表能耗: {e}")

# 8. 数据时间范围 - 修复方法
try:
    print(f"\n=== 数据时间信息 ===")
    # 从第一个电表获取时间范围
    first_meter = elec.meters[0]
    timeframe = first_meter.get_timeframe()
    print(f"时间范围: {timeframe}")
    print(f"开始时间: {timeframe.start}")
    print(f"结束时间: {timeframe.end}")
    duration = timeframe.end - timeframe.start
    print(f"数据持续时间: {duration.days}天 {duration.seconds // 3600}小时")
except Exception as e:
    print(f"无法获取时间范围: {e}")

# 9. 可视化分析
print(f"\n=== 生成可视化图表 ===")

# 创建图表
fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# 9.1 设备类型分布饼图
device_counts = {k: len(v) for k, v in device_stats.items() if k != "主电表"}
if device_counts:
    axes[0, 0].pie(device_counts.values(), labels=device_counts.keys(), autopct='%1.1f%%')
    axes[0, 0].set_title('设备类型分布')

# 9.2 电表数量柱状图
categories = list(device_counts.keys())
counts = list(device_counts.values())
bars = axes[0, 1].bar(categories, counts)
axes[0, 1].set_title('各类设备数量')
axes[0, 1].tick_params(axis='x', rotation=45)
axes[0, 1].set_ylabel('数量')

# 为柱状图添加数值标签
for bar in bars:
    height = bar.get_height()
    axes[0, 1].text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom')

# 9.3 尝试绘制能耗分布
try:
    energy_per_meter = elec.submeters().energy_per_meter()
    if not energy_per_meter.empty and 'active' in energy_per_meter.index:
        active_energy = energy_per_meter.loc['active'].dropna()

        # 准备数据用于可视化
        energy_values = []
        energy_labels = []

        for meter_id, energy in active_energy.items():
            energy_values.append(energy)
            if hasattr(meter_id, 'instance'):
                energy_labels.append(f'电表{meter_id.instance}')
            else:
                energy_labels.append(str(meter_id))

        # 能耗分布柱状图
        bars = axes[1, 0].bar(range(len(energy_values)), energy_values)
        axes[1, 0].set_title('各电表能耗分布')
        axes[1, 0].set_xlabel('电表')
        axes[1, 0].set_ylabel('能耗 (kWh)')
        axes[1, 0].set_xticks(range(len(energy_labels)))
        axes[1, 0].set_xticklabels(energy_labels, rotation=45)

        # 为柱状图添加数值标签
        for i, bar in enumerate(bars):
            height = bar.get_height()
            axes[1, 0].text(bar.get_x() + bar.get_width() / 2., height,
                            f'{energy_values[i]:.1f}', ha='center', va='bottom')

        # 能耗占比饼图 - 只显示前10个最大的
        sorted_energy = sorted(zip(energy_labels, energy_values), key=lambda x: x[1], reverse=True)
        top_10_labels, top_10_values = zip(*sorted_energy[:10])

        axes[1, 1].pie(top_10_values, labels=top_10_labels, autopct='%1.1f%%')
        axes[1, 1].set_title('能耗占比分布 (前10名)')

except Exception as e:
    print(f"无法生成能耗图表: {e}")
    # 如果能耗图表失败，显示设备统计
    device_items = list(device_counts.items())
    if device_items:
        labels, values = zip(*device_items)
        axes[1, 0].bar(labels, values)
        axes[1, 0].set_title('设备数量统计')
        axes[1, 0].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('nilmtk_analysis.png', dpi=300, bbox_inches='tight')
plt.show()

# 10. 电表层次结构总结
print(f"\n=== 电表层次结构总结 ===")
print(f"总电表数: {len(elec.meters)}")
print(f"  ├─ 主电表: {len(mains.meters)}个")
print(f"  ├─ 嵌套组: {len(nested)}组 (包含{sum(len(g.meters) for g in nested)}个电表)")
print(f"  └─ 普通子电表: {len(submeters.meters) - sum(len(g.meters) for g in nested)}个")

# 11. 能耗排名
try:
    print(f"\n=== 能耗排名 (前10名) ===")
    energy_per_meter = elec.submeters().energy_per_meter()
    if not energy_per_meter.empty and 'active' in energy_per_meter.index:
        active_energy = energy_per_meter.loc['active'].dropna()

        # 创建能耗排名
        energy_ranking = []
        for meter_id, energy in active_energy.items():
            if hasattr(meter_id, 'instance'):
                actual_id = meter_id.instance
                meter = elec[actual_id]
                if meter.appliances:
                    app_type = meter.appliances[0].type
                    if isinstance(app_type, dict):
                        device_name = app_type.get('type', f'电表{actual_id}')
                    else:
                        device_name = str(app_type)
                else:
                    device_name = f'电表{actual_id}'
                energy_ranking.append((device_name, actual_id, energy))
            else:
                energy_ranking.append((str(meter_id), str(meter_id), energy))

        # 按能耗排序
        energy_ranking.sort(key=lambda x: x[2], reverse=True)

        for i, (device_name, meter_id, energy) in enumerate(energy_ranking[:10], 1):
            print(f"  {i:2d}. {device_name} (电表{meter_id}): {energy:.2f} kWh")

except Exception as e:
    print(f"无法生成能耗排名: {e}")

# 12. 尝试获取功率数据样本 - 简化版本
print(f"\n=== 功率数据样本 ===")
try:
    print("尝试加载主电表功率数据...")
    # 使用更简单的方法加载数据
    main_meter = mains.meters[0]  # 获取第一个主电表

    # 加载少量数据进行展示
    power_data = next(main_meter.load(chunksize=100))  # 只加载100个数据点
    print(f"主电表功率数据形状: {power_data.shape}")
    print("前5行数据:")
    print(power_data.head())

    print(f"数据列: {power_data.columns.tolist()}")
    print(f"数据类型: {power_data.dtypes}")

except Exception as e:
    print(f"无法加载功率数据: {e}")

print(f"\n=== 分析完成 ===")
