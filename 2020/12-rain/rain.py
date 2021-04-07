""" Day 12: Rain Risk """
import os
import sys


CHARS = 'NSEWLRF'


def parse_line(text):
    """ parse line into (operator, argument) tuple. """
    action, value = text[0], int(text[1:])
    if action not in CHARS:
        raise ValueError('invalid action %r' % action)
    if value < 0:
        raise ValueError('invalid value %r' % (value,))
    if action in 'LR' and (value % 90 != 0):
        raise ValueError('invalid value for action %r: %r' % (action, value))
    return action, value


def parse_file(fd):
    """ read instructins from a file-like object. """
    for lineno, line in enumerate(fd, 1):
        try:
            yield parse_line(line.rstrip())
        except Exception as e:
            raise ValueError('error on line %d (%r): %s' % (lineno, line, e))


def distance(position, initial=(0, 0)):
    """ Get the manhattan distance between two points. """
    return abs(position[0] - initial[0]) + abs(position[1] - initial[1])


def move(position, op):
    """ Move position according to an operation. """
    x, y = position[:2]
    heading, n = op
    if heading == 'N':
        y += n
    elif heading == 'S':
        y -= n
    elif heading == 'E':
        x += n
    elif heading == 'W':
        x -= n
    else:
        raise ValueError('invalid heading %r' % (heading,))
    return (x, y) + position[2:]


headings = ('E', 'N', 'W', 'S')
directions = {'R': -1, 'L': 1}


def turn(state, op):
    """ Change direction. """
    current = state[-1]
    direction, degrees = op

    idx = headings.index(current)
    steps = (degrees // 90) * directions[direction]
    current = headings[(idx + steps) % len(headings)]

    return state[:-1] + (current,)


transform = {
    'R': lambda p: (p[1], p[0] * -1) + p[2:],
    'L': lambda p: (p[1] * -1, p[0]) + p[2:],
}


def rotate(waypoint, op):
    """ Rotate waypoint. """
    direction, degrees = op
    tr = transform[direction]
    for _ in range(degrees // 90):
        waypoint = tr(waypoint)
    return waypoint


def follow(state, op):
    """ Move in current direction. """
    direction = state[-1]
    return move(state, (direction, op[1]))


def towards(position, waypoint, op):
    """ Move towards waypoint. """
    _, factor = op
    delta = waypoint[0] * factor, waypoint[1] * factor
    return position[0] + delta[0], position[1] + delta[1]


def travel_state(state, ops):
    """ Travel according to headings. """
    for op in ops:
        if op[0] in directions:
            state = turn(state, op)
        elif op[0] in headings:
            state = move(state, op)
        elif op[0] == 'F':
            state = follow(state, op)
        else:
            raise ValueError('invalid op: %r' % (op,))
    return state


def travel_waypoint(position, waypoint, ops):
    """ Travel according to waypoints. """
    for op in ops:
        if op[0] in transform:
            waypoint = rotate(waypoint, op)
        elif op[0] in headings:
            waypoint = move(waypoint, op)
        elif op[0] == 'F':
            position = towards(position, waypoint, op)
        else:
            raise ValueError('invalid op: %r' % (op,))
    return position, waypoint


default_input_file = os.path.join(os.path.dirname(__file__), 'input.txt')


def main(inargs=None):
    filename = (sys.argv + [default_input_file])[1]

    with open(filename) as f:
        ops = tuple(parse_file(f))

    initial_state = (0, 0, 'E')
    final_state = travel_state(initial_state, ops)
    d = distance(final_state, initial_state)
    print(f"Part 1: {d}")

    initial_pos, initial_wp = ((0, 0), (10, 1))
    final_pos, final_wp = travel_waypoint(initial_pos, initial_wp, ops)
    d = distance(final_pos, initial_pos)
    print(f"Part 2: {d}")


if __name__ == '__main__':
    main()
