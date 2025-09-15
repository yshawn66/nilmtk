#实验 1 在redd数据集上选取特定电气进行CO算法测试
from nilmtk.api import API              #从NILMTK库中导入API模块
from nilmtk.disaggregate import CO      #从NILMTK的disaggregate模块中导入CO算法
import warnings
import os

warnings.filterwarnings("ignore")

# 数据路径
data_path = os.path.join('..', 'data', 'redd_low.h5')

# 最简实验配置
experiment = {
    'power': {'mains': ['apparent'], 'appliance': ['active']},      #设置了要使用的功率类型
    'sample_rate': 60,                                              #采样率设置
    'appliances': ['fridge', 'dish washer'],                        #目标电器设置
    'methods': {"CO": CO({})},                                      #算法选择
    'train': {                                                      #训练数据配置
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {1: {'start_time': '2011-04-18', 'end_time': '2011-04-20'}}
            }
        }
    },
    'test': {                                                       #测试数据配置
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {1: {'start_time': '2011-05-01', 'end_time': '2011-05-02'}}
            }
        },
        'metrics': ['rmse']                                         #使用RMSE（均方根误差）作为准确性评估指标
    }
}

# 运行实验
print("运行 NILMTK 实验...")
results = API(experiment)

# 显示结果
if results.errors:
    error_df = results.errors[0]
    print("\n📊 RMSE 结果:")
    for appliance in error_df.index:
        rmse = error_df.loc[appliance, 'CO']
        print(f"{appliance}: {rmse:.2f}")

print("✅ 实验完成")
