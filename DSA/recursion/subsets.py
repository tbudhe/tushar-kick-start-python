class Solution:
    # [[],[1],[2],[1,2]]
    def subsets_iterative(self, nums: list[int])->list[list[int]]:
        result = [[]]
        for num in nums:
            # 1,2
            for box in result[:]:
                # []->[]
                # []+[1]->[1]
                # []+[2]->[2]
                # [1]+[2]->[1,2] 
                result.append(box + [num])
                # [],[1],[2],[1,2]
        return result


    # [[], [1], [1, 2], [2]]
    def subsets_lexicographic(self, nums: list[int]) -> list[list[int]]:
        result = []
        n = len(nums)
        def dfs(start=0, path=[]):
            result.append(path[:])
            for i in range(start, n):
                path.append(nums[i])
                dfs(i+1)
                path.pop()
        dfs()

        return result
    # [[1, 2], [1], [2], []]
    def subsets_default(self, nums: list[int])->list[list[int]]:
            result = []
            n = len(nums)
            def dfs(path=[], start=0):
                if start == n:
                    result.append(path[:])
                    return
                path.append(nums[start])
                dfs(path, start+1)
                path.pop()
                dfs(path, start+1)
            dfs()
            
            return result
    # [[], [2], [1], [1, 2]]
    def subsets_binary(self, nums: list[int])->list[list[int]]:
        result = []
        n = len(nums)
        def dfs(path=[], start=0):
            if start == n:
                result.append(path[:])
                return
    
            dfs(path, start+1)
            path.append(nums[start])
            dfs(path, start+1)
            path.pop()
        dfs()
        
        return result

solution = Solution()
print(solution.subsets_iterative([1,2]))