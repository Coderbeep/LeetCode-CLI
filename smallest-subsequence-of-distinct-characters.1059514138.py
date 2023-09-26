class Solution:
    def smallestSubsequence(self, s: str) -> str:
                
        # This will store the last occurences of letters
        occurences = {}
        for i in range(len(s)):
            occurences[s[i]] = i

        stack = []
        used = set()

        for i in range(len(s)):
            # If letter not used, 
            if s[i] not in used:
                while stack and s[i] < stack[-1] and occurences[stack[-1]] > i:
                    used.remove(stack.pop())
                
                stack.append(s[i])
                used.add(s[i])
            # If letter already used, go to the next iteration    
            else:
                continue
        
        return ''.join(stack)