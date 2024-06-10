import math
import random
import statistics

lst = [10, 34, 4, 65, 5, 23, 8, 61, 92, 7]
sum_lst = math.fsum(lst)
arithmetic_mean_lst = statistics.fmean(lst)
median_lst = statistics.median(lst)
lst_dev = statistics.stdev(lst)
random_num_lst = random.choice(lst)
random_nums_lst = random.sample(lst, 5)
print(lst)
print(sum_lst)
print(arithmetic_mean_lst)
print(median_lst)
print(lst_dev)
print(random_num_lst)
print(random_nums_lst)