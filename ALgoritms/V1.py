# -----------a1----------------

def searchInsert(nums, target):
    for i, j in enumerate(nums):
        if target == j:
            return(i)
        elif target < j and i == 0:
            return(0)
        elif target < j+1:
            return(i)
    return(len(nums))


n = searchInsert([0, 1, 3, 5], 6)

# -----------a2----------------


def strStr(haystack, needle):
    if needle == '':
        return 0
    else:
        for i, j in enumerate(haystack):
            if len(haystack[i:]) < len(needle):
                return -1
            elif j == needle[0]:
                if haystack[i:i+len(needle)] == needle:
                    return i
        return -1


answer = strStr('hello', '')
print(answer)