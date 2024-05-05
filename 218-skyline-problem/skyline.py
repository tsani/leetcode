example_input = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
example_output = [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]

example_input_2 = [[0,2,3],[2,5,3]]

import heapq
from dataclasses import dataclass
from typing import Literal

@dataclass
class Building:
    left: int
    right: int
    height: int

    def __lt__(self, other):
        return self.left < other.left

@dataclass
class Event:
    kind: Literal['start', 'end']
    building: Building

    @property
    def x(self):
        if self.kind == 'start':
            return self.building.left
        elif self.kind == 'end':
            return self.building.right
        else:
            raise RuntimeError('impossible')

def in_batches(events):
    batch = []
    for e in events:
        if not len(batch) or batch[0].x == e.x:
            batch.append(e)
        else:
            # print('emit batch', batch)
            yield batch
            batch = [e]
    if len(batch): yield batch

def events(buildings):
    buildings = [
        Building(left, right, height)
        for left, right, height
        in buildings
    ]
    active_buildings = []
    def push_bldg(b):
        heapq.heappush(active_buildings, (b.right, b))
    def pop_bldg():
        return heapq.heappop(active_buildings)[1]
    def peek_right():
        return active_buildings[0][0] if len(active_buildings) else float('inf')

    for b in buildings:
        while True:
            active = peek_right()
            if active <= b.left:
                e = Event('end', pop_bldg())
                # print('event', e)
                yield e
            else:
                break
        push_bldg(b)
        e = Event('start', b)
        # print('event', e)
        yield e

    while len(active_buildings):
        yield Event('end', pop_bldg())

def go(buildings):
    heights = []
    def peek_height():
        return -heights[0][0] if len(heights) else 0
    def push_bldg(b):
        heapq.heappush(heights, (-b.height, b))
    def pop_bldg():
        return heapq.heappop(heights)[1]
    def remove_bldg(b):
        if not len(heights): raise RuntimeError('impossible')
        v = pop_bldg()
        # print('remove', b, 'is', v, '?')
        if v is b: return None
        remove_bldg(b)
        push_bldg(v)

    for evs in in_batches(events(buildings)):
        assert len(evs), 'event batch is nonempty'
        item = None
        if len(evs) > 1:
            print('handling batch with size > 1', evs)
        for e in evs:
            current = peek_height()
            if e.kind == 'start':
                push_bldg(e.building)
                # print('pushed', e.building)
                new = peek_height()
                if new > current:
                    item = (e.x, new)
            elif e.kind == 'end':
                remove_bldg(e.building)
                # print('removed', e.building)
                new = peek_height()
                if current != new:
                    item = (e.x, new)
        if item is not None:
            yield item

class Solution(object):
    # def getSkyline(self, buildings):
    #     return list(go(buildings))
    def getSkyline(self, buildings):
        res = []
        last = None
        current_height = 0
        for x in go(buildings):
            if last is None or last[0] == x[0]:
                last = x
            else:
                if last[1] != current_height:
                    res.append(last)
                    current_height = last[1]
                last = x
        res.append(last)
        return res

if __name__ == '__main__':
    print(Solution().getSkyline(example_input_2))
