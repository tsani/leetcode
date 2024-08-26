# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

import heapq

# Smart solution: use a heap to track which is the next smallest item to emit
class Solution:
    def mergeKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        head = None
        tail = None

        # Idea: use a priority queue on tuples (N, I) where N is the value of
        # the linked list at index I.
        # Populate the initial queue by traversing the list and storing all
        # nonempty lists.
        # Then pump the queue to decide which list to advance next.
        # If that list is nonempty, insert its next item into the queue.

        h = []

        for i, l in enumerate(lists):
            if l is None: continue
            heapq.heappush(h, (l.val, i))

        while len(h):
            (val, i) = heapq.heappop(h)
            if head is None:
                head = ListNode(val, None)
                tail = head
            else:
                tail.next = ListNode(val, None)
                tail = tail.next
            lists[i] = lists[i].next
            if lists[i] is not None:
                heapq.heappush(h, (lists[i].val, i))

        return head
