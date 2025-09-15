from nilmtk import DataSet
import os

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

# 1. 所有电表
print("所有电表：")
print(elec)

# 2. 主电表
print("\n主电表：")
print(elec.mains())

# 3. 子电表
print("\n子电表：")
print(elec.submeters())

# 4. 嵌套电表组
print("\n嵌套电表组：")
print(elec.nested_metergroups())

# 5. 主电表功率数据（简单方法）
print("\n主电表功率数据：")
try:
    main_meter = elec.mains().meters[0]
    data = next(main_meter.load(chunksize=5))
    print(data)
except:
    print("数据加载失败")
