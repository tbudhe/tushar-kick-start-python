class Solution:
    def combine(self, n: int, k: int) -> list[list[int]]:
        result = []
        stack_count = 0
        def dfs(start=1, path=[]):
            nonlocal stack_count
            stack_count += 1
            if len(path) == k:
                result.append(path[:])
                return result
            if start == n+1:
                return result
            for i in range(start, n+1):
                path.append(i)
                dfs(i+1, path)
                path.pop()
        dfs()
        print(f"combine count : {stack_count}")
        return result

    def combine_optimize(self, n: int, k: int) -> list[list[int]]:
        result = []
        stack_count = 0
        def dfs(start=1, path=[]):
            nonlocal stack_count
            stack_count += 1
            if len(path) == k:
                result.append(path[:])
                return result
            need = k - len(path)
            for i in range(start, n-need+2):
                path.append(i)
                dfs(i+1, path)
                path.pop()
        dfs()
        print(f"combine_optimize count : {stack_count}")

        return result


solution = Solution()
print(solution.combine(4, 2))
print(solution.combine(4, 3))
print(solution.combine_optimize(4, 2))
print(solution.combine_optimize(4, 3))
