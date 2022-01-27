# class Solution:
#     def searchInsert(self, nums: List[int], target: int) -> int:


# for i, j in [([1,2 3,4], 5)]:
#     print(searchInsert(nums=i, target=j))


def searchInsert(nums, target):
    for i, j in enumerate(nums):
        if target < j:
            if i > 0:
                return i-1
            else:
                return -1
        elif target == j:
            return i
        elif target > j

# searchInsert([0, 1, 4], )
print(range(-7, 8))