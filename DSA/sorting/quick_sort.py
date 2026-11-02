# 2026-10-31 — quick sort (Lomuto partition), written by Tushar.
# FIX OWED: quick_sort() has no return -> print shows None. See SORTING_NOTES.md.

def partition(nums, low, high):
    pivot = nums[high]
    i = low - 1
    for j in range(low, high):
        if (nums[j] <= pivot):
            i += 1
            nums[j], nums[i] = nums[i], nums[j]
    nums[i + 1], nums[high] = nums[high], nums[i + 1]
    return i+1


def quick_sort_helper(nums, low, high):
    if low < high:
        pi = partition(nums, low, high)
        # Recursively sort elements before and after partition
        quick_sort_helper(nums, low, pi - 1)
        quick_sort_helper(nums, pi + 1, high)


def quick_sort(nums):
    quick_sort_helper(nums, 0, len(nums)-1)


print(quick_sort([4, 7, 8, 5, 2, 3, 1, 9]))


