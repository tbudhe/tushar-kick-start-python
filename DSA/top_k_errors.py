from collections import defaultdict,Counter
class Solution:
    def top_k_errors(self,logs: list[str], k: int) -> list[str]:
        dict_logs = Counter(logs)
        return sorted(dict_logs.keys(),key=lambda c: (-dict_logs[c],c))[:k]
        result = []
        for log in dict_logs.keys():
            if dict_logs.get(log) >=k and len(result)<=k:
                result.append(log)
        return result

solution = Solution()
# logs = ["E500", "E404", "E500", "E401", "E404", "E500"], k = 2
# → ["E500", "E404"]

# logs = ["B", "A", "B", "A", "C"], k = 2
# → ["A", "B"]   # tie on count 2, so alphabetical order

# logs = ["X"], k = 1
# → ["X"]
print(solution.top_k_errors( ["E500", "E404", "E500", "E401", "E404", "E500"],2))
print(solution.top_k_errors(  ["B", "A", "B", "A", "C"],2))
print(solution.top_k_errors( ["X"],1))