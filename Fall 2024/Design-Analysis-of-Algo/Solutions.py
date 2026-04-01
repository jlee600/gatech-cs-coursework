# DO NOT ADD ANY IMPORTS
from typing import *

class Solutions:
    # DO NOT MODIFY INIT
    def __init__(self):
        pass

    # Problem 1: Real Estate Profits
    # Explanation and Runtime:
    #   My algorithm employs DP table of size n x n where dp[i][j] represents the maximum profit possible by selling the property ranging from i to j.
    #   Base case: dp[i][i] = values[i-1] * value[i] * value[i+1], where out-of-bounds holds the value equivalent to 1. 
    #              As dp[i][i] is only selling one property, no need for the recurrence
    #   Recurrence: for all k in [i,j], max((values[i-1] * value[i] * value[j+1]) + dp[i][k-1] + dp[k+1][j]), where dp[i][k-1] is the max profit for the
    #               for the properties left to the k, and dp[k+1][j] is that of the properties right to the k.
    #   Final answer: could be retrieved at dp[0][n-1]
    #   Reasoning: The DP table works because it breaks the problem into many subproblems, solving smaller ranges first (using base cases)
    #              and building up to the full range. This ensures that every possible selling order is considered, and the maximum profit for each subrange
    #              is correctly computed and reused.
    #   Runtime: There are n^2 cells to fill out due to the size of n x n dp table, and each cell takes O(n) time due to k times considerations. 
    #            Therefore, the overall runtime is O(n^3).
    def realEstatePrices(values: List[int]) -> int:
        n = len(values)
        # dp table size of n x n
        dp = [[0] * n for i in range(n)]
        for length in range(1, n + 1):
            for left in range(n - length + 1):
                right = left + length - 1
                for i in range(left, right + 1):
                    left_val = 1 if left == 0 else values[left - 1]
                    right_val = 1 if right == n - 1 else values[right + 1]
                    profit = left_val * values[i] * right_val
                    left_profit = dp[left][i - 1] if i > left else 0
                    right_profit = dp[i + 1][right] if i < right else 0
                    dp[left][right] = max(dp[left][right], profit + left_profit + right_profit)
        return dp[0][n - 1]
    # print(realEstatePrices([5,1,8,3]))
    
    # Problem 2: Warehouse Package Stacking
    # Explanation and Runtime:
    #   The algorithm first sorts the packages by width in ascending order and, for equal widths, in decreasing order of height. This way, it ensures that two packages 
    #   with the same width cannot be stacked, and the problem is reduced to finding the LIS of the heights. (I have used python's sort() as it is more efficient 
    #   than using nested loop - sort() takes O(nlogn) while nested loops takes O(n^2), which yields time out) The algorithm calculates the LIS by performing a binary search 
    #   every time through the sorted packages (more efficient than LIS algorithm from the lecture). It keeps a list, called heights, where each element is the smallest 
    #   possible ending height of an increasing subsequence of a given length. The algorithm performs a binary search for every package to find the very first position 
    #   in heights where the current package's height can replace an existing value so that the subsequence remains optimized for future heights. If the current height 
    #   is larger than all values in heights, it is appended to extend the sequence. The length of the heights list at the end will represent the maximum number of packages 
    #   that can be stacked together.
    #   Runtime: O(nlogn), where n is the number of elements in the list, as sort() in python uses Timsort algo that costs O(nlogn) and 
    #   finding the LIS takes another O(nlogn) time. 
    def maxPackages(packages: List[Tuple[int, int]]) -> int:
        def binary_search(arr: List[int], target: int) -> int:
            left, right = 0, len(arr)
            while left < right:
                mid = (left + right) // 2
                if arr[mid] >= target:
                    right = mid
                else:
                    left = mid + 1
            return left
        if not packages:
            return 0
        #sort packages first based on the width in ascending order, then height in descending order
        packages.sort(key=lambda x: (x[0], -x[1]))
        heights = []
        for i, height in packages:
            idx = binary_search(heights, height)
            if idx == len(heights) or len(heights) == 0:
                heights.append(height)
            else:
                heights[idx] = height
        return len(heights)
    # print(maxPackages([[5, 4], [6, 4], [6, 7], [2, 3]]))
    # print(maxPackages([[8, 9], [1, 1], [6, 10], [3, 4], [5, 8], [2, 3]]))

    # Problem 3: Building Blocks
    # Explanation and Runtime: 
    #   The algorithm uses DP table size of 2 x n to determine the minimum number of swaps required to make both arrays strictly increasing. 
    #   The dp values are initialized with Integer.MAXVALUE (float('inf') in python) for it to be compared during recurrence and produce the minimum value.
    #   The first row represents the minimum swaps needed if no swap is performed, and the second row presents the same thing but when the swap is performed.
    #   Basecase: dp[0][0] = 0, dp[1][0] = 1: At index 0, if no swap required -> 0, if swap required -> 1 
    #   Recurrence: dp[0][i] = dp[0][i-1] and dp[1][i] = dp[1][i-1] + 1 if nums1 and nums2 are already both strictly increasing 
    #               dp[0][i] = dp[1][i - 1] and dp[1][i] = dp[0][i - 1] + 1 if swap required to keep both nums1 and num2 strictly increasing 
    #   Final Answer: could be retrieved by taking minimum value from the last column as dp table is filled from left to right, and rightmost column covers every numbers.
    #                 if the result value is still float('inf'), it means that they were no solutions and therefore returns -1.
    #   Runtime: O(n) as filling in each cell takes constant time and there are total of n cells.
    def minSwap(nums1: List[int], nums2: List[int]) -> int:
        n = len(nums1)
        # Integer.MAX_VALUE = float('inf')
        dp = [[float('inf')] * n for i in range(2)]
        dp[0][0] = 0  
        dp[1][0] = 1
        for i in range(1, n):
            if nums1[i] > nums1[i - 1] and nums2[i] > nums2[i - 1]:
                dp[0][i] = min(dp[0][i], dp[0][i - 1])
                dp[1][i] = min(dp[1][i], dp[1][i - 1] + 1)
            if nums1[i] > nums2[i - 1] and nums2[i] > nums1[i - 1]:
                dp[0][i] = min(dp[0][i], dp[1][i - 1])
                dp[1][i] = min(dp[1][i], dp[0][i - 1] + 1)
        result = min(dp[0][n - 1], dp[1][n - 1])
        return -1 if result == float('inf') else result
    # print(minSwap([3, 4, 5, 4], [1, 2, 3, 8])) 
    # print(minSwap([3, 4, 5, 6], [1, 2, 3, 8]))

    # Problem 4: Modular Two Sum 
    # Explanation and Runtime:
    #   The array is processed by iterating through each element and calculating its remainder when divided by k. In order to acquire positive remainder value 
    #   (e.g -4 % 6 = 2), we add k to (num % k) and mod it with k once again. Then, frequency of each remainder are stored in count_rem. 
    #   Purpose: Two number's sum will be divisible by k iff their remainders add up to the multiple of k (including 0).
    #   Since remainder 0 implies that any combination of such numbers will by divisible by k, we use the math formula (n * (n-1)) / 2 for calculation. If the number if even,
    #   the remainder of half of its value also forms the pairs itself. Any other cases will be handled by multiplying itself to the frequency of complementary.
    #   Runtime: O(n) where n is the length of the array as it iterates the list once and performs calculations that take constant time.
    def modTwoSum(A: List[int], k: int) -> int:
        if k < 2 or len(A) < 2:
            return -1
        count_rem = [0] * k
        for num in A:
            rem = ((num % k) + k) % k
            count_rem[rem] += 1
        result = (count_rem[0] * (count_rem[0] - 1)) // 2
        for i in range(1, (k + 1) // 2):
            result += count_rem[i] * count_rem[k - i]
        if k % 2 == 0:
            result += (count_rem[k // 2] * (count_rem[k // 2] - 1)) // 2
        return result
    #print(modTwoSum([5, 7, 1, 10, -4, 119], 6))

    # Problem 5: Maximum Magic Path Power
    # Explanation and Runtime:
    #
    #
    def maximumMagicPathPower(energies: List[int], edges: List[List[int]], maxTime: int) -> int:
        graph: Dict[int, List[tuple[int, int]]] = {}
        visited = {}  
        max_power = [energies[0]]  
        curr_path = [0]
        return max_power[0]
    # energies = [0, 32, 10, 43]
    # edges = [[0,1,10], [1,2,15], [0,3,10]]
    # maxTime = 49
    # print(maximumMagicPathPower(energies,edges,maxTime))

    # Problem 6: Divide the Harvest
    # Explanation and Runtime:
    #
    #
    def divideTheHarvest(quantity: List[int], k: int) -> int:
        left = min(quantity)  # Minimum possible sum
        right = sum(quantity)  # Maximum possible sum
        result = 0
        return result

    # print(divideTheHarvest([1, 2, 3, 4, 5, 6, 7, 8, 9], 5))

    # Problem 7: Coloring Sidewalks 
    # Explanation and Runtime:
    #   The algorithm uses dp table size of n x 3 to minimize the total painting time while ensuring no two adjacent sidewalks have the same color.
    #   dp[i][j] represents the min time required to paint the first i+1 sidewwalks with ith sidewalk painted with j color.
    #   Basecase: minimum time to color the first sidewalk is whatever the value is for each color. Therefore, dp[0][i] = time[0][i]
    #   Recurrence: For each sidewalk, we calculate the minimum cost by adding the cost of painting the previous sidewalk in a different color 
    #               to ensure no two adjacent sidewalks share the same color. This could be done by dp[color] = min(dp[prev_other color1], dp[prev_other color2]) + time[color]
    #   Final answer: could be retrived by getting the minimum of dp table's last row as it it is filled from the top all the way to the bottom.
    #   Runtime: O(n) as each computations to fill in the cells takes constant time and there are 3n cells total (O(3n) = O(n)).
    def coloringSidewalks(time: List[int]) -> int:
        n = len(time)
        dp = [[0] * 3 for i in range(n)]
        dp[0][0] = time[0][0]  # Gold
        dp[0][1] = time[0][1]  # White
        dp[0][2] = time[0][2]  # Blue
        for i in range(1, n):
            dp[i][0] = min(dp[i-1][1], dp[i-1][2]) + time[i][0]  
            dp[i][1] = min(dp[i-1][0], dp[i-1][2]) + time[i][1]  
            dp[i][2] = min(dp[i-1][0], dp[i-1][1]) + time[i][2] 
        return min(dp[n-1][0], dp[n-1][1], dp[n-1][2])
    #print(coloringSidewalks([[3,2,5],[3,4,6],[3,1,2]]))

    # Problem 8: Chemical Concoctions
    # Explanation and Runtime:
    #
    #
    def chemicalConcoctions(formulas: List[str]) -> str:
        return ""

    # Problem 9: Maximum Sum of Non-Adjacent Subsequences
    # Explanation and Runtime:
    #   The algorithm uses a DP table size of n to store the maximum sum of non-adjacent subsequences, where dp[i] represents the maximum sum 
    #   within the first but non-adjacent i+1 elements of the array A.
    #   Basecase: dp[0] = A[0] as the maximum possible sum value for the first elemnent is just first element itself.
    #             dp[1] = max(A[0], A[1]) as we are choosing only one between the first two values (pertaining to non-adjacent constraint)
    #   Recurrence: each time, we consider whether to add the number or not. Therefore, we could take the bigger values between yes and no.
    #               dp[i] = A[i] + dp[i-2] if yes: we add that number to the dp value at 2 steps behind it (non-adjacent)
    #               dp[i] = dp[i-1] if no: we don't add and just take the previous one
    #               -> max(dp[i-1], A[i] + dp[i-2]
    #   Final answer: Since the last cell in dp table considers every possible element in A, it could be retrieved at dp[n-1]
    #   Runtime: O(n) as each cells takes constant time to fill in and there are total of n cells.
    def maxNonAdjSum(A: List[int]) -> int:
        n = len(A)
        if n == 0:
            return 0
        elif n == 1:
            return A[0]
        dp = [0] * n
        dp[0] = A[0]  
        dp[1] = max(A[0], A[1]) 
        for i in range(2, n):
            dp[i] = max(dp[i-1], A[i] + dp[i-2])
        return dp[n-1]
    # print(maxNonAdjSum([3]) 
    # print(maxNonAdjSum([3, 2]) 
    # print(maxNonAdjSum([3, 2, 7, 10])) 
    # print(maxNonAdjSum([3, 5, 1, 9, 8]))  
    # print(maxNonAdjSum([4, 1, 1, 4, 2, 1]))  

    # Problem 10: DigitGPT
    # Explanation and Runtime: 
    #   First, the algorithm sorts the ticket string into two halves: the left and right parts. The key idea for the solution is to calculate 
    #   the sum of digits in each half, count the number of '*' in each half, then using those counts decide whether the sums can be balanced.
    #   It is possible to balance it, if and only if, the total number of '*' are even in number (to make pairs) and difference between sums can be 
    #   compensated by the maximum contribution of the '*' characters. The algorithm will return True if the difference between the sums can be complemented 
    #   using * characters; otherwise, it returns False.
    #   Runtime: O(n) as it iterates the ticket list once to calculate the sum of left half and the right half as well as the number of stars in the string.
    def reviveStrings(n: int, ticket: str) -> bool:
        if (n != len(ticket)):
            return False
        sum_left, sum_right = 0, 0
        left = ticket[:n//2]
        right = ticket[n//2:]
        for i in left:
            if i != '*':
                sum_left += int(i)
        for i in right:
            if i != '*':
                sum_right += int(i)
        star_left, star_right = left.count('*'), right.count('*')
        total = star_left + star_right
        diff = abs(sum_left - sum_right)
        maxStar = 9 * min(star_left, star_right)
        remain = (abs(star_left - star_right) // 2) * 9
        # if total % 2 == 0: 
        #     if diff <= maxStar:
        #         return True
        #     return False
        # else:  
        #     return False
        return diff <= (maxStar + remain)
    # print(reviveStrings(3,'2433'))
    # print(reviveStrings(4,'2433'))
    # print(reviveStrings(6,'00*0*0'))
    # print(reviveStrings(10,'7****55555'))
    # print(reviveStrings(6,'000**0'))
    # print(reviveStrings(8,'18*2*903'))
    # print(reviveStrings(6,'**2641'))

    # Problem 11: Building a Brick Wall
    # Explanation and Runtime: 
    #   The algorithm uses dp table size l + 1 where l is the length of the wall. It basically utilizes Knapsack problem to find the number of ways 
    #   to build a wall of length l. DP table dp[i] represents the number of ways to construct a wall of length i.
    #   Base case: dp[0] = 1 because there is only one way to construct a wall of length 0, and that is using no bricks.
    #   Recurrence: dp[j] += dp[j - b]: We can construct a wall of length j by appending a brick of length b at the end of a wall of length j−b. 
    #               The above recurrence ensures that all possible brick combinations have been considered.
    #   Final answer: could be retrieved dp[l] as it gives the total total number of ways to construct a wall of length l.
    #   Time complexity: O(l x B) where l is the length of the wall and B is the length of array B. Since this algorithm takes every brick in B into consideration 
    #   and computes values for wall lengths <= l.
    def buildBrickWall(B: List[int], l: int) -> int:
        dp = [0] * (l + 1)
        dp[0] = 1
        for b in B:
            for j in range(b, l + 1):
                dp[j] += dp[j - b]
        return dp[l]
    # print(buildBrickWall([1, 2, 5], 6))  
    # print(buildBrickWall([3, 5], 7))     
    # print(buildBrickWall([1], 3))        
    # print(buildBrickWall([2, 3], 6))

    # Problem 12: Archipelagos
    # Explanation and Runtime:
    #
    #
    def findNeededBridges(n: int, edges: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
        if (n is None or edges is None):
            return False
        return []

    # Problem 13: Search Engineer 
    # Explanation and Runtime: 
    #   This algorithm uses dp table of size n + 1, where n is the length of the pattern, to determine how many distinct ways the pattern appears as a subsequence in the text.
    #   Specfically, dp[i] represents the count of subsequences for the first i characters of the pattern in the text. In other words, dp[3] would represent the number of ways 
    #   the first three characters of the pattern appear as subsequences.
    #   Base case: dp[0] = 1 since there is only one way to match an empty pattern: selecting no characters.
    #   Recurrence: For each character in text, if text[i−1] equals pattern[j−1], then dp[j] adds the value of dp[j−1] because it extends the subsequences 
    #   including pattern[j−1]; otherwise, dp[j] doesn't change. This counts every subsequence matching while maintaining correctness for overlapping subproblems.
    #   Final answer: could be retrieved at dp[len of the pattern] as it gives the total number of distinct subsequences of the entire pattern in the text.
    #   Runtime: O(m x n) where m is the length of the text and n is that of the pattern. This is because we run a loop for all the characters in the pattern 
    #   for each character in the text.
    def numDistinct(text: str, pattern: str) -> int:
        len_text, len_pattern = len(text), len(pattern)
        if len_pattern == 0:
            return 1
        if len_text == 0:
            return 0
        dp = [0] * (len_pattern + 1)
        dp[0] = 1 
        for i in range(1, len_text + 1):
            for j in range(len_pattern, 0, -1):
                if text[i - 1] == pattern[j - 1]:
                    dp[j] += dp[j - 1]
        return dp[len_pattern]
    # print(numDistinct('rabbbit', 'rabbit'))
    # print(numDistinct("aaaa", "aa"))

    # Problem 14: Buzz's Bees
    # Explanation and Runtime:
    #
    #
    def minNetworkCost(coords: list[tuple[int, int]]) -> int:
        return -1
