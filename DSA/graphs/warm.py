from collections import deque,defaultdict
# A.
queue = deque()
queue.append((0, 0))
r, c = queue.popleft()
queue.append((r + 1, c))
print(queue)
# B.
visited = set()
visited.add("hit")
print("hit" in visited)
print("hot" in visited)
# C.
size = len(queue)
for i in range(size):
    print(f"processing {i}")
# D.
edges = [[0, 1], [0, 2], [1, 2]];
graph = defaultdict(list)      # missing key → auto-creates []
for a, b in edges: 
  graph[a].append(b);
# console.log(graph.get(0));   // [1, 2]
# console.log(graph.get(5));   // undefined
# E.
word = "hit"
for i in range(len(word)) :
  pattern = word[0:i] + "*" + word[i + 1:]
  print(pattern)
# F.
grid = [[0]*3 for _ in range(2)]
grid[0][0] = 1
print(grid);   