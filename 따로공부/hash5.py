nums = [1, 3, 3, 2, 2, 2, 4]

count = {}

for num in nums:
    if num in count:
        count[num] = count.get(num, 0) + 1
    else:
        count[num] = 1

max_num = None
max_value = 0

for key, value in count.items():
    if value > max_value:
        max_value = value
        max_num = key

print(max_num)  

print(count.get(max_num))
