from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        st = 0
        en = len(nums)-1
        while st < en:
            curr_sum = nums[st] + nums[en]
            if curr_sum == target:
                return [st+1, en+1]
            elif curr_sum < target:
                st += 1
            else:
                en -= 1
        return [-1, -1]


solution = Solution()
print(solution.twoSum([2, 7, 8, -4], 9))
