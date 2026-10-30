from collections import defaultdict, deque
import copy


class Solution:

    def words_ladder_problem(self,begin, end, words):
        graph = defaultdict(list)
        if(end not in words):
            return 0
        collection_words = copy.deepcopy(words)
        collection_words.append(begin)
        collection_words.sort()

        def compare_patterns(left, right) -> bool:
            min_length = min(len(left), len(right))
            for i in range(min_length):
                left_pattern = left[0:i] + "*" + left[i+1:]
                right_pattern = right[0:i] + "*" + right[i+1:]
                if right_pattern == left_pattern:
                    return True
            return False
        for i in range(len(collection_words)):
            for j in range(i+1, len(collection_words)):
                previous_word = collection_words[i]
                current_word = collection_words[j]
                if compare_patterns(previous_word, current_word):
                    graph[previous_word].append(current_word)
                    graph[current_word].append(previous_word)
        queue = deque([(begin, 1)])
        visited = {begin}
        while len(queue) > 0:
            word, distance = queue.popleft()
            if (word == end):
               return distance
            if word in graph:
                neighbors = graph.get(word)
                for neighbor in neighbors:
                    if neighbor not in visited:
                        queue.append((neighbor, distance+1))
                        visited.add(neighbor)
        return 0
# Graph
# hit->hot, hot->[dot,lot], dot-> lot , lot->log dog->[log,cog] , log->cog
# hit -> hot -> dot ->lot ->log->coh
# hit -> hot -> lot
# # test1
# beginWord, endWord = "hit", "cog"
# wordList = ["hot","dot","dog","lot","log","cog"]   # -> 5

# # test2: "cog" is not in the list, so it can't be reached
# wordList = ["hot","dot","dog","lot","log"]         # -> 0

# # test3
# beginWord, endWord = "a", "c"
# wordList = ["a","b","c"]                           # -> 2
solution = Solution()
print(solution.words_ladder_problem("hit","cog",["hot","dot","dog","lot","log","cog"]))
print(solution.words_ladder_problem("hit", "cog", ["hot","dot","dog","lot","log"]))
print(solution.words_ladder_problem("a", "c", ["a","b","c"]))