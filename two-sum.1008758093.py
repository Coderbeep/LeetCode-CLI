class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        seen_numbers = {}
        for index, number in enumerate(nums):
            complement = target - number
            if complement in seen_numbers:
                return [index, seen_numbers[complement]] 
            else:
                seen_numbers[number] = index
        return None