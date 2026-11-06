class Solution:
    def find_pair(self,amounts: list[int], target: int) -> list[int]:
        amounts_index = {}
        for i,amount in enumerate(amounts):
            difference = target - amount
            if amount in amounts_index:
                return [amounts_index[amount],i]
            amounts_index[difference] = i
        return []
solution = Solution()
print(solution.find_pair([20, 50, 30, 70],100))
print(solution.find_pair([5, 5],10))
print(solution.find_pair([1, 4, 6, 9],10))