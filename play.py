from typing import List


class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        # Initialize a table to store the minimum cost for each day
        table = [0] * len(days)
        table[0] = min(costs)  # Minimum cost for the first day

        for i in range(1, len(days)):
            # Case 1: Buy a 1-day ticket
            case1 = table[i-1] + costs[0]

            # Case 2: Buy a 7-day ticket
            j = i - 1
            while j >= 0 and days[j] >= days[i] - 6:
                j -= 1
            case2 = table[j] + costs[1] if j >= 0 else costs[1]

            # Case 3: Buy a 30-day ticket
            j = i - 1
            while j >= 0 and days[j] >= days[i] - 29:
                j -= 1
            case3 = table[j] + costs[2] if j >= 0 else costs[2]

            # Update the table with the minimum cost for day i
            table[i] = min(case1, case2, case3)

        # Return the minimum cost for all days
        return table[-1]


# Example usage
solution = Solution()
days = [1, 4, 6, 7, 8, 20]
costs = [2, 7, 15]
print(solution.mincostTickets(days, costs))  # Output: 11
