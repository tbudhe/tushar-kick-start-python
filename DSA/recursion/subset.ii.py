class Solution:
    def subsetsWithDup(self, nums: list[int]) -> list[list[int]]:
        n = len(nums)
        result = []
        nums.sort() 
        def dfs(start, path):
            result.append(path[:])
            for i in range(start, n):
                if i > start and nums[i-1] == nums[i]:
                    continue
                path.append(nums[i])
                dfs(i+1,path)
                path.pop()
        dfs(0, [])
        return result


solution = Solution()
print(solution.subsetsWithDup([1, 2, 2]))
print(solution.subsetsWithDup( [0]))
print(solution.subsetsWithDup( [4, 4, 4, 1, 4]))
# Example 1

# Input:  nums = [1, 2, 2]
# Output: [[], [1], [1,2], [1,2,2], [2], [2,2]]

# Example 2

# Input:  nums = [0]
# Output: [[], [0]]

# Example 3

# Input:  nums = [4, 4, 4, 1, 4]
# Output: [[], [1], [1,4], [1,4,4], [1,4,4,4], [1,4,4,4,4],
#          [4], [4,4], [4,4,4], [4,4,4,4]]
