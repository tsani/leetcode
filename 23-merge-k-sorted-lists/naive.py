# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next


# Naive solution: take the min element of the list at each stage and emit that.
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        head = None
        tail = None

        while len(lists):
            min_i = -1
            min_x = float('inf')
            to_delete = [] # delete exhausted lists as a small speedup

            for i, l in enumerate(lists):
                if l is None:
                    to_delete.append(i)
                    continue
                if l.val < min_x:
                    min_i = i
                    min_x = l.val

            if min_i == -1: break # all lists were empty so we're done

            m = lists[min_i]
            lists[min_i] = m.next

            for i in reversed(to_delete): del lists[i]

            if head is None:
                head = ListNode(m.val, None)
                tail = head
            else:
                new_tail = ListNode(m.val, None)
                tail.next = new_tail
                tail = new_tail

        return head
