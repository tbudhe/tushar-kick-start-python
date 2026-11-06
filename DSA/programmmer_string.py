# Example(source, want, exc_msg=None, lineno=0, indent=0, options=None)
# programmerxxxprozmerqgram
from collections import Counter
import copy
def is_sum_match(map):
    sum = 0
    for key in map.keys():
        value = map.get(key)
        sum += value
    return sum<=0
def programmerStrings(s: str) -> int:
    programmer = "programmer"
    s_original = Counter(programmer)
    s_deep_copy = copy.deepcopy(s_original)
    n = len(s)
    m = n//2
    left = 0
    for i in range(m):
        if s[i] in programmer:
            s_original[s[i]] -=1
            if is_sum_match(s_original):
                left = i+1
                break
    for i in range(n-1,m,-1):
        if s[i] in programmer:
            s_deep_copy[s[i]] -=1
            if is_sum_match(s_deep_copy):
                right = i
                return right - left
    return 0
print(programmerStrings("programmerxxxprozmerqgram")) #3
print(programmerStrings("progxrammerrxproxgrammer"))#2
print(programmerStrings("xprogxrmaxemrppprommograeiruu"))#2
print(programmerStrings("programmerprogrammer"))#0
