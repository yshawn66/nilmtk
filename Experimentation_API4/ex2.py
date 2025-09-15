# 实验2：多算法比较 - REDD数据集（修复版）
from nilmtk.api import API
from nilmtk.disaggregate import CO, Mean, FHMMExact  # 正确的导入
import warnings
import os

warnings.filterwarnings("ignore")

# 数据路径
data_path = os.path.join('..', 'data', 'redd_low.h5')

# 多算法实验配置
experiment2 = {
    'power': {'mains': ['apparent'], 'appliance': ['active']},
    'sample_rate': 60,
    'appliances': ['fridge', 'dish washer', 'microwave'],
    'methods': {
        "Mean": Mean({}),
        "CO": CO({}),
        "FHMM": FHMMExact({'num_of_states': 2})  # 使用正确的类名
    },
    'train': {
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {1: {'start_time': '2011-04-18', 'end_time': '2011-04-20'}}
            }
        }
    },
    'test': {
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {1: {'start_time': '2011-05-01', 'end_time': '2011-05-02'}}
            }
        },
        'metrics': ['mae', 'rmse']
    }
}

# 运行实验
print("运行多算法比较实验...")
results = API(experiment2)

# 显示结果
if results.errors:
    for i, error_df in enumerate(results.errors):
        metric = results.errors_keys[i].split('_')[-1]
        print(f"\n📊 {metric.upper()} 结果:")
        for appliance in error_df.index:
            print(f"{appliance}:")
            for method in error_df.columns:
                value = error_df.loc[appliance, method]
                print(f"  {method}: {value:.2f}")

print("✅ 实验完成")
