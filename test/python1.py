
import math

def segregate(arr):
    return [x for x in arr if x%2 == 0] + [x for x in arr if x%2 != 0]


arr = [1, 8, 5, 3, 2, 6, 7, 10]
arr1 = [1,2,3,4]
# List comprehension
arr = segregate(arr)
print(arr)
print(arr+arr1)

# slicing: list[start_index : end_index : step_size]
print(arr[2::])
print(arr[2::2])

# lambda:
square_root = lambda x: math.sqrt(x)
print(square_root(4))
def square_root_2(x):
    return math.sqrt(x)
print(square_root_2(4))

# map: tra ve kq sau ap dung ham/lambda qua 1 CHUOI PHAN TU
map1 = list(map(lambda x: x*x,sorted(arr)))
print(map1)

# filter: tra ve cac PHAN TU sau khi thuc hien ham/lambda tra ve TRUE
filter1 = list(filter(lambda x: x%2==0, arr))
print(filter1)
