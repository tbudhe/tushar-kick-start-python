class Solution:
    def permutations(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        result = []
        n = len(nums)
        used = [False]*n
        path = []

        def dfs():
            if len(path) == n:
                result.append(path[:])
                return result
            for i in range(n):
                if i > 0 and nums[i] == nums[i - 1] and not used[i-1]:
                    continue
                if used[i]:
                    continue
                used[i] = True
                path.append(nums[i])
                dfs()
                path.pop()
                used[i] = False
        dfs()
        return result


solution = Solution()
print(solution.permutations([1, 2, 3]))
print(solution.permutations([1, 1, 2]))
