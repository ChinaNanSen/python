import numpy as np
import time

# 使用 for 循环计算每个元素的平方
start_time = time.time()
squared = []
# 创建一个 NumPy 数组
arr = np.array(range(1,200000000))
# 使用向量化操作计算每个元素的平方
res = arr ** 2
end_time = time.time()
print(end_time - start_time,"秒")