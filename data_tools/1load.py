from nilmtk import DataSet
import os
# 加载数据集
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')
iawe = DataSet(data_path)

elec = iawe.buildings[1].elec

# 查看电表组
print(elec)

# 获取冰箱设备
fridge = elec['fridge']

# 查看可用测量列
print(fridge.available_columns())

# 使用load()加载数据
data = next(fridge.load())
print(data)

#数据集结构查看（显示了iAWE数据集建筑1中的12个电表；每个电表关联的设备类型（冰箱、空调、洗衣机等；识别了主电表（site_meter）和各个设备电表）
#测量的7个电气参数
#实际数据的加载