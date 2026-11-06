from typing import List


class Solution:
    def rob(self, nums: List[int]) -> int:
        n = len(nums)

        def dfs(st):
            if st >= n:
                return 0
            include = 0
            exclude = 0
            include = nums[st] + dfs(st+2)
            exclude = dfs(st+1)
            return max(include, exclude)
        return dfs(0)

    def robII(self, nums: List[int]) -> int:
        n = len(nums)
        dp = [0]*n
        if n == 0:
            return 0
        if n == 1:
            return nums[0]
        dp[0] = nums[0]
        dp[1] = max(nums[0], nums[1])
        for i in range(2, n):
            dp[i] = max(nums[i] + dp[i-2], dp[i-1])
        return max(dp[n-1], dp[n-2])


if __name__ == "__main__":
    s = Solution()
    assert s.robII([1, 2, 3, 1]) == 4        # rob house 0 + house 2 → 1 + 3
    assert s.robII([2, 7, 9, 3, 1]) == 12    # 2 + 9 + 1
    assert s.robII([5]) == 5                 # edge: one house
    assert s.robII([]) == 0                  # edge: no houses
    assert s.robII([1, 2, 0, 5]) == 7
    assert s.robII([1, 2, 5, 1]) == 6
    assert s.robII([1, 2, 5, 1, 9]) == 15
    print("All tests passed")
