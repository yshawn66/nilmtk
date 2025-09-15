from nilmtk import DataSet
import matplotlib.pyplot as plt
import os
import warnings

warnings.filterwarnings('ignore')


def load_data_demo():
    # 加载数据
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(current_dir, '..', 'data', 'iawe.h5')

    if not os.path.exists(data_path):
        print("❌ 数据文件不存在！")
        return

    iawe = DataSet(data_path)
    fridge = iawe.buildings[1].elec['fridge']

    print("🔍 可用数据列:", fridge.available_columns())

    # 测试各种加载方法
    methods = [
        ("所有列", lambda: next(fridge.load())),
        ("功率序列", lambda: next(fridge.power_series())),
        ("有功功率", lambda: next(fridge.load(ac_type='active'))),
        ("重采样60s", lambda: next(fridge.load(ac_type='active', sample_period=60)))
    ]

    results = {}
    for name, method in methods:
        try:
            data = method()
            results[name] = data
            shape = data.shape if hasattr(data, 'shape') else len(data)
            print(f"✅ {name}: {shape}")
        except Exception as e:
            print(f"❌ {name}: {e}")

    # 修复绘图部分
    if results:
        plt.figure(figsize=(12, 8))
        for i, (name, data) in enumerate(results.items(), 1):
            plt.subplot(2, 2, i)

            # 修复数据提取逻辑
            if hasattr(data, 'iloc'):  # DataFrame
                if len(data.shape) == 2 and data.shape[1] > 0:
                    plot_data = data.iloc[:500, 0]  # 取第一列
                else:
                    plot_data = data.iloc[:500]  # 单列DataFrame
            else:  # Series
                plot_data = data[:500]

            plt.plot(plot_data)
            plt.title(f'{name}\n数据量: {len(plot_data)}')
            plt.ylabel('功率 (W)')
            plt.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.show()

    # 显示数据详情
    print("\n📊 数据详情:")
    for name, data in results.items():
        print(f"\n{name}:")
        print(f"  类型: {type(data)}")
        if hasattr(data, 'columns'):
            print(f"  列名: {data.columns.tolist()}")
        print(f"  前3个值: {data.head(3).values.flatten()}")


if __name__ == "__main__":
    load_data_demo()
