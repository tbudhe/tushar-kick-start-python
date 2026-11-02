# LC 252 Meeting Rooms — 2026-10-31, written by Tushar.
class Solution:
    @staticmethod
    def hasConflicts(end,start)->bool:
        return end>start
    def meeting_rooms(self,nums:list):
        nums.sort(key=lambda x:x[0])
        for i in range(1,len(nums)):
            previous_meeting = nums[i-1]
            current_meeting = nums[i]
            if(Solution.hasConflicts(previous_meeting[1],current_meeting[0])):
                return False
        return True

solution = Solution()
print(solution.meeting_rooms([(0,30),(5,10),(15,20)]))  # False
print(solution.meeting_rooms([(5,8),(9,15)]))           # True
