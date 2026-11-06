from collections import defaultdict
from typing import List


class Solution:

    def build_graph(self,prerequisites:List[List[int]]):
        graph = defaultdict(list)
        for course in prerequisites:
            source, destination = course
            graph[source].append(destination)
        return graph
    def can_finish(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        graph = self.build_graph(prerequisites)
        visited = set()
        arrival = [0] * num_courses
        departure = [0] * num_courses
        ts = 0
        def dfs(node):
            visited.add(node)
            nonlocal ts
            ts += 1          
            arrival[node] = ts
            neighbors = graph[node]
            for neighbor in neighbors:
                if neighbor not in visited:
                    if dfs(neighbor) :
                        return True
                elif arrival[neighbor] > departure[neighbor]:
                         return True
                else:
                    continue
            ts +=1
            departure[node] = ts
            return False
        for i in range(num_courses):
           if i not in visited:
               if dfs(i):
                   return False
        return True

if __name__ == "__main__":
    solution = Solution()
    assert solution.can_finish(4, [[1, 0], [2, 1], [3, 2]]) is True
    assert solution.can_finish(2, [[1, 0], [0, 1]]) is False
    assert solution.can_finish(1, []) is True
    assert solution.can_finish(3, [[1, 0], [2, 0]]) is True
    assert solution.can_finish(3, [[1, 0], [2, 0], [2, 1]]) is True
    print("All tests passed")