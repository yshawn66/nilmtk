from nilmtk import DataSet
from nilmtk.elecmeter import ElecMeterID
import nilmtk
import matplotlib.pyplot as plt
import os

# 加载数据
current_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(current_dir, '..', 'data', 'redd_low.h5')
redd = DataSet(data_path)
elec = redd.buildings[1].elec

# 1. 数据质量分析
print("=== 数据质量分析 ===")
fridge_meter = elec['fridge']
good_sections = fridge_meter.good_sections(full_results=True)
dropout_rate = fridge_meter.dropout_rate()

plt.figure(figsize=(12, 4))
good_sections.plot()
plt.title('Data Quality (Blue = Good Data, White = Gaps)')
plt.show()

print(f"数据丢失率: {dropout_rate*100:.2f}%")
print(f"有效数据段数量: {len(good_sections.combined())}")

# 2. 单个电表选择方法
print("\n=== 单个电表选择 ===")

# 通过设备名称选择
fridge = elec['fridge']  # 默认实例1
light_2 = elec['light', 2]  # 指定实例2
print(f"冰箱: {fridge.appliances[0].type} (实例{fridge.instance})")
print(f"灯具2: {light_2.appliances[0].type} (实例{light_2.instance})")

# 通过实例号直接选择
main_meter = elec[1]  # 实例1通常是主电表
print(f"实例1电表: {'主电表' if main_meter.is_site_meter() else '子电表'}")

# 使用ElecMeterID全局选择
socket_meter = nilmtk.global_meter_group[ElecMeterID(
    instance=8, building=1, dataset='REDD'
)]
if socket_meter.appliances:
    print(f"插座电表: {socket_meter.appliances[0].type}")

# 3. 按类别选择设备
print("\n=== 按类别选择 ===")

# 单相感应电机设备
motor_devices = nilmtk.global_meter_group.select_using_appliances(
    building=1, category='single-phase induction motor'
)
print(f"单相感应电机设备: {len(motor_devices.meters)}个")

# 洗衣设备
laundry_devices = nilmtk.global_meter_group.select_using_appliances(
    building=2, category='laundry appliances'
)
print(f"洗衣设备: {len(laundry_devices.meters)}个")

# 4. MeterGroup选择
print("\n=== MeterGroup选择 ===")

# 选择多个电表组成MeterGroup
meter_group = elec[[
    ElecMeterID(instance=3, building=1, dataset='REDD'),
    ElecMeterID(instance=4, building=1, dataset='REDD')
]]
print(f"选择的电表组: {len(meter_group.meters)}个电表")

# 选择主电表
mains = elec.mains()
print(f"主电表数量: {len(mains.meters)}")

# 验证两种主电表选择方法等价
mains_by_id = elec[ElecMeterID(instance=0, building=1, dataset='REDD')]
print(f"两种主电表选择方法等价: {mains.meters == mains_by_id.meters}")

# 5. 按电表属性选择
print("\n=== 按属性选择 ===")

# 按设备型号选择
whole_house = elec.select(device_model='REDD_whole_house')
print(f"全屋电表: {len(whole_house.meters)}个")

# 按采样周期选择
sample_3s = elec.select(sample_period=3)
print(f"3秒采样电表: {len(sample_3s.meters)}个")

# 6. 系统概览
print(f"\n=== 系统概览 ===")
print(f"总子电表数: {len(elec.submeters().meters)}")
print(f"主电表数: {len(elec.mains().meters)}")
print(f"所有电表数: {len(elec.meters)}")
