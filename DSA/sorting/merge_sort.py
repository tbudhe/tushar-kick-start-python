# 2026-10-31 — merge sort, written by Tushar.

def merge(nums,left,right):
    i = 0
    j = 0
    k = 0
    nl = len(left)
    nr = len(right)
    while i<nl and j<nr:
        # <= stable sorting
        if left[i]<=right[j]:
            nums[k] = left[i]
            i+=1
        else:
            nums[k] = right[j]
            j+=1
        k+=1
    while i<nl:
        nums[k] = left[i]
        i+=1
        k+=1
    while j<nr:
        nums[k] = right[j]
        j+=1
        k+=1
    return nums
def merge_sort(nums:[int]):
    if len(nums) <= 1:
        return nums
    mid = len(nums)//2
    left = merge_sort(nums[:mid])
    right = merge_sort(nums[mid:])
    return merge(nums,left,right)
        
print(merge_sort([4,7,8,5,2,3,1,9]))
