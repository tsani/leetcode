def decompose(num: int):
    rem = num % 10
    quot = num // 10
    return (quot, rem)

NUMERALS = ['I', 'V', 'X', 'L', 'C', 'D', 'M']

def ten_to_numeral(k):
    """Gets the numeral for the given power of ten."""
    return NUMERALS[k*2]

def ten_to_five(k):
    return NUMERALS[k*2 + 1]

class Solution:
    def intToRoman(self, num: int) -> str:
        out = ''
        ten = 0
        while num > 0:
            num, rem = decompose(num)
            if rem < 4:
                out = rem * ten_to_numeral(ten) + out
            elif rem == 4:
                out = ten_to_numeral(ten) + ten_to_five(ten) + out
            elif rem == 5:
                out = ten_to_five(ten) + out
            elif rem < 9:
                out = ten_to_five(ten) + (rem - 5) * ten_to_numeral(ten) + out
            elif rem == 9:
                out = ten_to_numeral(ten) + ten_to_numeral(ten+1) + out
            else:
                assert False, 'fuck'
            ten += 1
        return out

if __name__ == '__main__':
    s = Solution()
    for i in range(50):
        print(s.intToRoman(i))
