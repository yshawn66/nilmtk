# 实验3：跨数据集4算法性能大比拼
from nilmtk.api import API
from nilmtk.disaggregate import CO, Mean, FHMMExact, Hart85
import warnings
import os
import pandas as pd

warnings.filterwarnings("ignore")

print("🚀 实验3：跨数据集4算法性能大比拼")
print("训练: REDD数据集 (美国) → 测试: UK-DALE数据集 (英国)")
print("算法: Mean, CO, FHMM, Hart85")
print("目标设备: fridge, microwave, dish washer")
print("评估指标: MAE + RMSE")
print("-" * 60)

# 跨数据集实验配置
experiment3_cross = {
    'power': {'mains': ['apparent'], 'appliance': ['active']},
    'sample_rate': 60,
    'appliances': ['fridge', 'microwave', 'dish washer'],  # 两个数据集都有的设备
    'methods': {
        "Mean": Mean({}),
        "CO": CO({}),
        "FHMM": FHMMExact({'num_of_states': 2}),
        "Hart85": Hart85({})
    },
    'train': {
        'datasets': {
            'REDD': {
                'path': os.path.join('..', 'data', 'redd_low.h5'),
                'buildings': {
                    1: {'start_time': '2011-04-20', 'end_time': '2011-05-01'},
                    2: {'start_time': '2011-04-20', 'end_time': '2011-05-01'}
                }
            }
        }
    },
    'test': {
        'datasets': {
            'UKDALE': {  # 跨数据集测试！
                'path': os.path.join('..', 'data', 'ukdale.h5'),
                'buildings': {
                    1: {'start_time': '2013-05-01', 'end_time': '2013-05-02'}
                }
            }
        },
        'metrics': ['mae', 'rmse']
    }
}

print("正在运行跨数据集4算法比较...")
try:
    results = API(experiment3_cross)

    # 显示详细结果
    print("\n📊 跨数据集性能结果:")
    for i, error_df in enumerate(results.errors):
        metric = results.errors_keys[i].split('_')[-1]
        print(f"\n{metric.upper()} 结果 (REDD训练 → UK-DALE测试):")
        print(error_df.round(2))

    # 跨数据集泛化能力分析
    print("\n🌍 跨数据集泛化能力排名:")
    mae_df = results.errors[0]

    # 计算每个算法的平均MAE
    avg_performance = mae_df.mean().sort_values()

    for i, (algo, avg_mae) in enumerate(avg_performance.items(), 1):
        if avg_mae < 30:
            level = "🟢 优秀"
        elif avg_mae < 50:
            level = "🟡 良好"
        else:
            level = "🔴 需改进"
        print(f"  {i}. {algo:6}: 平均MAE {avg_mae:.2f} {level}")

    # 各设备最佳算法
    print(f"\n🏆 各设备跨数据集最佳算法:")
    for appliance in mae_df.index:
        best = mae_df.loc[appliance].idxmin()
        value = mae_df.loc[appliance].min()
        print(f"  {appliance:12}: {best:6} (MAE: {value:.2f})")

    # 跨数据集挑战分析
    print(f"\n💡 跨数据集挑战分析:")
    print(f"  📍 地理差异: 美国 vs 英国用电习惯")
    print(f"  🏠 建筑差异: 不同房屋结构和设备")
    print(f"  ⚡ 电网差异: 不同电压和频率标准")
    print(f"  📊 数据差异: 不同采样率和标注方式")

    print("\n✅ 跨数据集4算法比较完成！")
    print("💡 这是真正考验算法泛化能力的终极测试！")

except Exception as e:
    print(f"❌ 实验失败: {e}")
    print("💡 提示: 确保UK-DALE数据集已下载")

    # 备选方案：REDD内部跨建筑
    print("\n🔄 备选方案: REDD内部跨建筑测试")
    experiment3_backup = experiment3_cross.copy()
    experiment3_backup['test']['datasets'] = {
        'REDD': {
            'path': os.path.join('..', 'data', 'redd_low.h5'),
            'buildings': {
                3: {'start_time': '2011-04-18', 'end_time': '2011-04-20'},
                4: {'start_time': '2011-04-18', 'end_time': '2011-04-20'}
            }
        }
    }

    try:
        print("运行REDD跨建筑测试...")
        results_backup = API(experiment3_backup)

        for i, error_df in enumerate(results_backup.errors):
            metric = results_backup.errors_keys[i].split('_')[-1]
            print(f"\n{metric.upper()} (跨建筑):")
            print(error_df.round(2))

    except Exception as e2:
        print(f"备选方案也失败: {e2}")
