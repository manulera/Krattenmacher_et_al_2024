import numpy as np


# def bootstrap_mean(data, num_samples):
#     n = len(data)
#     idx = np.random.randint(0, n, (num_samples, n))
#     samples = data[idx]
#     return samples


# data = np.array([3, 5, 2, 8, 9, 1, 6, 4, 7, 10])

# for i in bootstrap_mean(data, 3):
#     print(i)


print(np.random.choice([1, 2, 3], 4, replace=True))
