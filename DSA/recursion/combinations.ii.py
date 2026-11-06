class Solution:
    def combinationSum2(self, candidates: list[int], target: int) -> list[list[int]]:
        n = len(candidates)
        candidates.sort()
        # 1,1,2,5,6,7,10
        result = []
        def dfs(start, path, target):
            if target == 0:
                result.append(path[:])
                return
            for i in range(start, n):
                if i>start and candidates[i-1] == candidates[i]  :
                    continue
                if  candidates[i]>target:
                    break
                path.append(candidates[i])
                dfs(i+1, path, target - candidates[i])
                path.pop()
        dfs(0, [], target)
        return result


solution = Solution()
print(solution.combinationSum2([10, 1, 2, 7, 6, 1, 5],  8))
    # Output: [[1,1,6], [1,2,5], [1,7], [2,6]]
print(solution.combinationSum2([3],  2))
    # Output: []
print(solution.combinationSum2([2, 5, 2, 1, 2],  5))
    # Output: [[1,2,2], [5]]


# [[1, 1, 6], [1, 2, 5], [1, 7], [1, 2, 5], [1, 7], [2, 6]]
# []
# [[1, 2, 2], [1, 2, 2], [1, 2, 2], [5]]