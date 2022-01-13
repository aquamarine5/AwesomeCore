from typing import List
from progress import Progresser


class ListNode:
    def __init__(self, val: int, next):
        self.val = val
        self.next = next

    def __str__(self) -> str:
        buffer = ''
        n = self
        while n.next != None:
            buffer += str(n.val)
            print(buffer)
            n = n.next
        buffer += str(n.val)
        return buffer


class twoListNodeReverseAndAdd:
    class Solution():
        def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
            return self.buildListNode(self.listNodeToInt(l1)+self.listNodeToInt(l2))

        def listNodeToInt(self, l: ListNode) -> int:
            buffer = ''
            bn = l
            while(bn != None):
                buffer = str(bn.val)+buffer
                bn = bn.next
            return int(buffer)

        def buildListNode(self, i: int) -> ListNode:
            s = list(str(i))
            s.reverse()
            print(s)
            buffer: ListNode = ListNode(s[0], None)
            master = buffer
            print(buffer)
            s.remove(s[0])
            print(s)
            for i in s:
                k = ListNode(int(i), None)
                buffer.next = k
                buffer = k
            return master

    def __init__(self):
        l1 = ListNode(1, ListNode(2, ListNode(3, None)))
        l2 = ListNode(4, ListNode(5, ListNode(6, None)))
        print(self.Solution().addTwoNumbers(l1, l2))


class findCenterNumber:
    class Solution:
        def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
            l = nums1+nums2
            l.sort()
            c = len(l)
            t = c/2
            if int(t) == t:
                return (l[int(t)]+l[int(t-1)])/2
            else:
                return l[int(t-0.5)]


class atoi:
    class Solution:
        def myAtoi(self, s: str) -> int:
            l = list(s)
            sr = s.replace(" ", "")
            isPositive = True
            numlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
            nl = numlist+["+", "-", " "]
            numBuffer = ''
            readingNumber = False
            ro = False
            rot = False
            if len(l) == 0:
                return 0
            elif l == [" "]:
                return 0
            elif l[0] not in nl:
                return 0
            elif sr == "":
                return 0
            elif sr[0] not in nl:
                return 0
            elif l[0] == " " and l[1] == "b":
                return 0
            else:
                for i in l:
                    if i in numlist:
                        if ro:
                            rot = True
                            ro = False
                        readingNumber = True
                        numBuffer += i
                    else:
                        if i == "+":
                            if ro or readingNumber or rot:
                                break
                            if (not ro) and readingNumber:
                                break
                            isPositive = True
                            ro = True
                        elif i == "-":
                            if ro or readingNumber or rot:
                                break
                            if (not ro) and readingNumber:
                                break
                            isPositive = False
                            ro = True
                        else:
                            if readingNumber:
                                break
                            elif ro:
                                break
            if numBuffer == "":
                numBuffer = 0
            o = int(numBuffer)
            overflow = False
            if o not in range(-2147483648, 2147483648):
                overflow = True
                o = 2147483647
            if not isPositive:
                o = -o
                if overflow:
                    o -= 1
            return o


class findMaxCallbackString:
    class OfficialDemo:
        def longestPalindrome(self, s: str) -> str:
            pass

    class Result:
        def __init__(self, de: int, ds: int, s: str) -> None:
            self.de = de
            self.ds = ds
            self.s = s
            self.r = de-ds

        def __str__(self) -> str:
            return f"de:{self.de};ds:{self.ds},s:{self.s}"

    class Solution:
        def longestPalindrome(self, s: str) -> str:
            l = list(s)
            buffer = []
            bufferI = []
            for i in l:  # i -> a,b,c,d
                ln = l.copy()
                ds = ln.index(i)
                c = ln.count(i)
                if c > 1:
                    for _ in range(c-1):
                        ln.remove(i)
                    de = ln.index(i)
                else:
                    de = ds-1
                buffer.append(findMaxCallbackString.Result(de, ds, i))
                bufferI.append(de-ds)
            bufferC = bufferI.copy()
            m = max(bufferI)
            bufferC.remove(m)
            ic = buffer[bufferC.count(m)]
            if m == -1 and len(s) == 1:
                return s
            if m == 0:
                return s
            return s[ic.ds:][:(ic.de+ic.ds)]


class isCallbackString:
    class Solution:
        def isPalindrome(self, x: int) -> bool:
            l = str(x)
            return l == l[::-1]


class reverseInt:
    class Solution:
        def reverse(self, x: int) -> int:
            s = list(str(x))
            c = False
            r = ""
            if s[0] == "-":
                s.remove("-")
                c = True
            s.reverse()
            for i in s:
                r += i
            j = int(r)
            if c:
                j = -j
            if j not in range(-2147483648, 2147483648):
                return 0
            return j


class containerWithMostWater:
    class Solution:

        def maxArea(self, height: List[int]) -> int:
            L = 0
            r = 0
            R = len(height)-1
            while L < R:
                a = min(height[L], height[R])*(R-L)
                r = max(r, a)
                if height[L] <= height[R]:
                    L += 1
                else:
                    R -= 1
            return r


class Sum2:
    class Solution:
        def twoSum_Sum3_Obsolete(self, ii: int, nums: List[int], rnums: List[int], target: int) -> List[List[int]]:
            s = ii+1
            e = len(nums)-1
            l = nums.copy()
            l.sort()
            t = []
            while(s < e):
                o = l[s]+l[e]
                if o == target:
                    r = rnums.copy()
                    i = r.index(l[s])
                    r[i] = None
                    j = r.index(l[e])
                    t.append([i, j])
                    while s < e and l[s] == l[s+1]:
                        s += 1
                    while s < e and l[e] == l[e-1]:
                        e -= 1
                    s += 1
                    e -= 1
                else:
                    if o > target:
                        e -= 1
                    elif o < target:
                        s += 1
            return t

        def twoSum(self, nums: List[int], target: int) -> List[int]:
            s = 0
            e = len(nums)-1
            l = nums.copy()
            l.sort()
            while(True):
                o = l[s]+l[e]
                if o > target:
                    e -= 1
                elif o < target:
                    s += 1
                else:
                    break
            i = nums.index(l[s])
            nums[i] = None
            j = nums.index(l[e])
            return [i, j]


class Sum3:
    class Solution:
        def threeSum_Obsolete(self, nums: List[int]) -> List[List[int]]:
            if len(nums) < 3:
                return []
            r = []
            # Progresser Start
            p = Progresser(len(nums)*len(nums))
            # Progresser End
            for i in range(len(nums)):
                for j in range(len(nums)):
                    p.print_slider_complex_animation_next()
                    if i >= j:
                        continue
                    ii = nums[i]
                    jj = nums[j]
                    n = nums.copy()
                    o = 0-ii-jj
                    n.remove(ii)
                    n.remove(jj)
                    if o in n:
                        r.append([ii, jj, o])
            rb = []
            for m in r:
                m.sort()
                if m not in rb:
                    rb.append(m)
            return rb

        def threeSum_Obsolete2(self, nums: List[int]) -> List[List[int]]:
            if len(nums) < 3:
                return []
            r = []
            neg = []
            pos = []
            hz = 0
            n = nums.copy()
            for d in n:
                print(d)
                if d > 0:
                    neg.append(d)
                elif d < 0:
                    pos.append(d)
                else:
                    hz += 1

            print(f"neg:{neg}")
            print(f"pos:{pos}")
            print(f"hz:{hz}")
            print(nums)
            if hz >= 3:
                r.append([0, 0, 0])
            for i in range(len(nums)):
                for j in range(len(nums)):
                    ii = nums[i]
                    jj = nums[j]
                    nn = neg.copy()
                    pp = pos.copy()
                    o = 0-ii-jj
                    print("i:", i, "j:", j, "o:", o)
                    if i >= j:
                        continue

                    if ii > 0:
                        nn.remove(ii)
                    elif ii < 0:
                        pp.remove(ii)
                    else:
                        hz -= 1
                    if jj > 0:
                        nn.remove(jj)
                    elif jj < 0:
                        pp.remove(jj)
                    else:
                        hz -= 1
                    ll = [ii, jj, o]

                    if o > 0:
                        if o in nn:
                            r.append(ll)
                    elif o < 0:
                        if o in pp:
                            r.append(ll)
                    else:
                        if hz >= 1:
                            r.append([ii, jj, 0])
                    return r
            rb = []
            for m in r:
                m.sort()
                if m not in rb:
                    rb.append(m)
            return rb

        def threeSum(self, nums: List[int]) -> List[List[int]]:
            r = []
            c = len(nums)
            if not nums or c < 3:
                return []
            nums.sort()
            for ii in range(c):
                i = nums[ii]
                s = ii+1
                e = len(nums)-1
                if i > 0:
                    return r
                if ii > 0 and i == nums[ii-1]:
                    continue
                while(s < e):
                    o = nums[s]+nums[e]+i
                    if (o == 0):
                        r.append([i, nums[s], nums[e]])
                        while s < e and nums[s] == nums[s+1]:
                            s += 1
                        while s < e and nums[e] == nums[e-1]:
                            e -= 1
                        s += 1
                        e -= 1
                    elif (o > 0):
                        e -= 1
                    else:
                        s += 1
            return r


class IntToRoman:
    class Solution:
        def t3(self, s3: str, v1: str, v5: str, v10: str) -> str:
            s3 = int(s3)
            r3 = ""
            if s3 < 4:
                r3 = v1*s3
            elif 4 <= s3 <= 5:
                r3 = v1*(5-s3)+v5
            elif 6 <= s3 <= 8:
                r3 = v5+v1*(s3-5)
            elif 9 <= s3 <= 10:
                r3 = v1*(10-s3)+v10
            return r3

        def intToRoman(self, num: int) -> str:
            l = list(str(num))
            c = len(l)
            r = ""
            if c == 4:
                s4 = int(l[0])*"M"
                s3 = self.t3(l[1], "C", "D", "M")
                s2 = self.t3(l[2], "X", "L", "C")
                s1 = self.t3(l[3], "I", "V", "X")
                r = s4+s3+s2+s1
            elif c == 3:
                s3 = self.t3(l[0], "C", "D", "M")
                s2 = self.t3(l[1], "X", "L", "C")
                s1 = self.t3(l[2], "I", "V", "X")
                r = s3+s2+s1
            elif c == 2:
                s2 = self.t3(l[0], "X", "L", "C")
                s1 = self.t3(l[1], "I", "V", "X")
                r = s2+s1
            elif c == 1:
                r = self.t3(l[0], "I", "V", "X")
            return r


class RomanToInt:
    class Solution:
        def romanToInt(self, s: str) -> int:
            buffer = 0
            l = len(s)
            for i in range(l):
                ii = s[i]
                if ii == "C":
                    if i+1 < l:
                        if s[i+1] == "D" or s[i+1] == "M":
                            buffer -= 100
                        else:
                            buffer += 100
                    else:
                        buffer += 100
                elif ii == "D":
                    buffer += 500
                elif ii == "M":
                    buffer += 1000
                elif ii == "L":
                    buffer += 50
                elif ii == "X":
                    if i+1 < l:
                        if s[i+1] == "L" or s[i+1] == "C":
                            buffer -= 10
                        else:
                            buffer += 10
                    else:
                        buffer += 10
                elif ii == "V":
                    buffer += 5
                elif ii == "I":
                    if (i+1) < l:
                        if s[i+1] == "V" or s[i+1] == "X":
                            buffer -= 1
                        else:
                            buffer += 1
                    else:
                        buffer += 1
            return buffer


class RegularExpressionMatching:
    class Solution:
        def isMatch(self, s: str, p: str) -> bool:
            l = list(s)
            x = len(p)
            b = None
            m = 0
            if p.count(".") == 0 and p.count("*") == 0 and p != s:
                return False
            for i in range(len(l)):
                t = l[i]
                c = p[m]
                m += 1
                print("i:", i, "t:", t, "m:", m, "c:", c, "b:", b)
                if t == b:
                    continue
                else:
                    b = None
                if c == "." or c == "*":
                    m += 1
                    continue
                else:
                    if i+1 < x:
                        if p[i+1] == "*":
                            m += 1
                            b = p[i]
                            print("PASSED SUCCESSED")
                            continue
                    print("FAILED")
                    if t != c:
                        return False
            return True

def BottleGuess():
    b=5
    f=5
    d=5
    while(f>=2 or d>=4):
        print(f,d)
        if f>=2:
            f-=2
            b+=1
            d+=1
            f+=1
        if d>=4:
            d-=4
            b+=1
            d+=1
            f+=1
    print(b,f,d)
BottleGuess()
