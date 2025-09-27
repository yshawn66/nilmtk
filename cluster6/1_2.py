# 导入必要的NILMTK库
from nilmtk import DataSet
from nilmtk.api import API
from nilmtk.disaggregate import CO
import warnings
import os

# 1. 加载数据集
print("加载数据集中...")

# 使用相对路径，从 cluster6 文件夹返回上一级，再进入 data 文件夹
data_path = os.path.join('..', 'data', 'redd_low.h5')

# 检查文件是否存在，给出更明确的提示
if not os.path.exists(data_path):
    raise FileNotFoundError(f"错误：在路径 '{os.path.abspath(data_path)}' 下找不到数据集文件。请检查 data_path 设置是否正确。")

print(f"成功定位数据集: {os.path.abspath(data_path)}")
dataset = DataSet(data_path)

# 2. 选择要分析的建筑和时间段 (这部分不影响API实验)
building_num = 1
dataset.set_window(start="2011-04-18", end="2011-05-21")
elec = dataset.buildings[building_num].elec

# 3. 定义要对比的算法
algorithms = {}

print("创建使用 K-Means 的 CO 算法实例...")
algorithms['CO_KMeans'] = CO({'clustering_algorithm': 'kmeans'})

print("创建使用 DBSCAN 的 CO 算法实例...")
algorithms['CO_DBSCAN'] = CO({'clustering_algorithm': 'dbscan'})

# 4. 设置并运行实验
# 定义实验参数
experiments = {
    'power': {
        'mains': ['apparent'],
        'appliance': ['active']
    },
    # ------------------- 修改部分开始 -------------------
    # 在原有基础上，加入了更多在数据集中存在的主要电器
    'appliances': [
        'fridge',
        'dish washer',
        'microwave',
        'washer dryer',
        'light',
        'electric oven',
        'electric stove',
        'electric space heater'
    ],
    # ------------------- 修改部分结束 -------------------
    'sample_period': 6,
    'train': {
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {
                    1: {
                        'start_time': '2011-04-18',
                        'end_time': '2011-04-30'
                    }
                }
            }
        }
    },
    'test': {
        'datasets': {
            'REDD': {
                'path': data_path,
                'buildings': {
                    1: {
                        'start_time': '2011-05-01',
                        'end_time': '2011-05-10'
                    }
                }
            }
        },
        'metrics': ['f1score', 'mae']
    },
    'methods': algorithms
}

# 创建 API 实例。
# NILMTK 的 API 在创建对象时就会自动执行所有训练和测试！
# 实验结果表格会在此时被打印出来。
print("\n正在初始化 NILMTK API 并开始执行实验...")
api = API(experiments)
print("实验执行完毕！")

# 5. 从 API 对象中提取结果并保存到变量中
print("\n--- 正在从已完成的实验中提取结果 ---")

# api.errors 是一个 DataFrame 的列表，api.errors_keys 是它们对应的名称列表。
# 我们使用 zip 将它们组合成一个字典，方便按名称访问。
results_dict = dict(zip(api.errors_keys, api.errors))

# 使用从调试信息中发现的、正确的键来提取数据
f1_scores_df = results_dict['REDD_1_f1score']
mae_df = results_dict['REDD_1_mae']

print("--- 结果已成功提取到 DataFrame 变量中 ---\n")

# 6. 打印从变量中捕获的结果，以确认成功
print("===============================================")
print("===   从变量中打印最终捕获的结果   ===")
print("===============================================\n")

print("--- F1 分数 (来自变量 f1_scores_df) ---")
print(f1_scores_df)

print("\n--- MAE (来自变量 mae_df) ---")
print(mae_df)

print("\n\n脚本已成功运行并捕获所有结果！")
