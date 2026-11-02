# LC 215 Kth Largest Element in an Array — 2026-10-31, written by Tushar.
import heapq
from typing import List   # added so the file runs outside LeetCode

class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        pq = []
        for num in nums:
            heapq.heappush(pq, num)
            if len(pq)>k:
                heapq.heappop(pq)
        return pq[0]
    def findKthLargestOld(self, nums: List[int], k: int) -> int:
        nums.sort(reverse=True)
        return nums[k-1]

print(Solution().findKthLargest([3,2,1,5,6,4], 2))          # 5
print(Solution().findKthLargest([3,2,3,1,2,4,5,5,6], 4))    # 4
