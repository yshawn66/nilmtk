# 实验3：扩展多算法比较 - REDD数据集（最简版）
from nilmtk.api import API
from nilmtk.disaggregate import CO, Mean, FHMMExact, Hart85
import warnings
import os
import pandas as pd

warnings.filterwarnings("ignore")

# 实验配置
experiment3 = {
    'power': {'mains': ['apparent'], 'appliance': ['active']},
    'sample_rate': 60,
    'appliances': ['fridge', 'dish washer', 'microwave', 'sockets', 'light'],
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
                    1: {'start_time': '2011-04-18', 'end_time': '2011-04-20'},
                    2: {'start_time': '2011-04-18', 'end_time': '2011-04-20'}
                }
            }
        }
    },
    'test': {
        'datasets': {
            'REDD': {
                'path': os.path.join('..', 'data', 'redd_low.h5'),
                'buildings': {
                    1: {'start_time': '2011-05-01', 'end_time': '2011-05-02'},
                    3: {'start_time': '2011-04-18', 'end_time': '2011-04-19'}
                }
            }
        },
        'metrics': ['mae', 'rmse']
    }
}

# 运行实验
print("🚀 实验3：扩展多算法比较")
results = API(experiment3)

# 显示结果
for i, error_df in enumerate(results.errors):
    metric = results.errors_keys[i].split('_')[-1]
    print(f"\n📊 {metric.upper()}:")
    print(error_df.round(2))

# 最佳算法
print("\n🏆 最佳算法:")
mae_df = results.errors[0]
for appliance in mae_df.index:
    best = mae_df.loc[appliance].idxmin()
    value = mae_df.loc[appliance].min()
    print(f"{appliance}: {best} ({value:.2f})")

print("\n✅ 完成")
