nums = [1, 2, 2, 3, 2, 3]
count = {}

# for num in nums:
#     if num in count:
#         count[num] += 1
#     else:
#         count[num] = 1


for num in nums:
    count[num] = count.get(num, 0) + 1
print(count)