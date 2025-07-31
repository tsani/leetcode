class Uneven(Exception):
    pass

class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if k <= 1 or head is None:
            return head

        acc = p = head
        p = p.next
        acc.next = None
        try:
            for i in range (k-1):
                if p is None:
                    raise Uneven()
                else:
                    print(p.val)
                    t = p.next
                    p.next = acc
                    acc = p
                    p = t
        except Uneven:
            p = acc
            acc = None
            while p is not None:
                t = p.next
                p.next = acc
                acc = p
                p = t
            return acc
        else:
            head.next = self.reverseKGroup(p, k)
            return acc