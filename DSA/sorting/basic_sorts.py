# 2026-10-31 — basic O(n^2) sorts, written by Tushar.
# NOTE: bubble_sort below is actually "exchange sort" (compares i with every j),
# not bubble sort (compares ADJACENT pairs). See SORTING_NOTES.md.

def selections_sort(nums: [int])-> [int]:
    n   =len(nums)
    for i in range(n):
        min_num = i
        for j in range(i+1,n):
            if nums[j]<nums[min_num]:
                min_num = j
        nums[min_num],nums[i] =nums[i],nums[min_num]
    return nums

# print(selections_sort([4,7,8,5,2,3,1,9]))

def bubble_sort(nums: [int])-> [int]:
    n   = len(nums)
    for i in range(n):
        for j in range(i+1,n):
            if nums[j]<nums[i]:
                nums[j],nums[i] =nums[i],nums[j]
    return nums

# print(bubble_sort([4,7,8,5,2,3,1,9]))


def insertion_sort(nums: [int])-> [int]:
    n   = len(nums)
    for i in range(1,n):
        ith_num = nums[i]
        j = i-1
        while j>=0 and nums[j]>ith_num:
            nums[j+1] = nums[j]
            j -=1
        nums[j+1] = ith_num
    return nums

print(insertion_sort([4,7,8,5,2,3,1,9]))
