import sys
import heapq
from collections import defaultdict
import itertools


def solve(lines: list[str]) -> int:
    types = 'ABCD'
    costs = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}
    room_positions = [2, 4, 6, 8]
    depth = len(lines) - 3
    room_lines = lines[2:2 + depth]

    rooms = [[] for _ in range(4)]
    for d in range(depth - 1, -1, -1):
        line = room_lines[d]
        for i in range(4):
            char = line[3 + 2 * i]
            if char in types:
                rooms[i].append(char)

    corridor = [None] * 11
    corr_line = lines[1]
    for i in range(11):
        char = corr_line[i + 1]
        if char in types:
            corridor[i] = char

    initial_corr = tuple(corridor)
    initial_rooms = tuple(tuple(room) for room in rooms)
    initial_state = (initial_corr, initial_rooms)

    target_rooms = tuple((types[i],) * depth for i in range(4))
    target_corr = (None,) * 11
    target_state = (target_corr, target_rooms)

    if initial_state == target_state:
        return 0

    dist = defaultdict(lambda: float('inf'))
    dist[initial_state] = 0
    pq = []
    count = itertools.count()
    heapq.heappush(pq, (0, next(count), initial_state))

    allowed_stops = [0, 1, 3, 5, 7, 9, 10]

    while pq:
        cost, _, state = heapq.heappop(pq)
        if cost > dist[state]:
            continue
        if state == target_state:
            return cost

        corr, rms = state

        # exit from rooms to corridor
        for ri in range(4):
            room = list(rms[ri])
            if not room:
                continue
            amph = room[-1]
            if amph == types[ri] and all(a == types[ri] for a in room):
                continue
            exit_pos = room_positions[ri]
            depth_out = depth - len(room) + 1
            for tp in allowed_stops:
                if corr[tp] is not None:
                    continue
                minp, maxp = min(exit_pos, tp), max(exit_pos, tp)
                if any(corr[p] is not None for p in range(minp + 1, maxp)):
                    continue
                steps = abs(tp - exit_pos) + depth_out
                move_cost = steps * costs[amph]
                new_corr = list(corr)
                new_corr[tp] = amph
                new_rooms = [list(r) for r in rms]
                new_rooms[ri] = room[:-1]
                new_state = (tuple(new_corr), tuple(tuple(r) for r in new_rooms))
                new_total = cost + move_cost
                if new_total < dist[new_state]:
                    dist[new_state] = new_total
                    heapq.heappush(pq, (new_total, next(count), new_state))

        # enter from corridor to rooms
        for cp in range(11):
            if corr[cp] is None:
                continue
            amph = corr[cp]
            ti = types.index(amph)
            enter_pos = room_positions[ti]
            minp, maxp = min(cp, enter_pos), max(cp, enter_pos)
            if any(corr[p] is not None for p in range(minp + 1, maxp)):
                continue
            room = rms[ti]
            if room and any(a != amph for a in room):
                continue
            steps_enter = depth - len(room)
            steps_corr = abs(cp - enter_pos)
            move_cost = (steps_corr + steps_enter) * costs[amph]
            new_corr = list(corr)
            new_corr[cp] = None
            new_rooms = [list(r) for r in rms]
            new_rooms[ti] = list(room) + [amph]
            new_state = (tuple(new_corr), tuple(tuple(r) for r in new_rooms))
            new_total = cost + move_cost
            if new_total < dist[new_state]:
                dist[new_state] = new_total
                heapq.heappush(pq, (new_total, next(count), new_state))

    return -1 # should not reach here


def main():
    lines = [line.rstrip('\n') for line in sys.stdin]
    result = solve(lines)
    print(result)


if __name__ == "__main__":
    main() # entry point