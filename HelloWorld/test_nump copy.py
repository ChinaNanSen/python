import numpy as np
import time

# # 创建一个数组
# arr = [1, 2, 3, 4, 5]

# 使用 for 循环计算每个元素的平方
start_time = time.time()
squared = []
for x in range(1,200000000):
    squared.append(x ** 2)
end_time = time.time()
print(end_time - start_time,"秒")

