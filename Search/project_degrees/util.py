from collections import deque

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action


class StackFrontier():
    def __init__(self):
        self.frontier = deque()
        self.states = set()

    def add(self, node):
        self.frontier.append(node)
        self.states.add(node.state)

    def contains_state(self, state):
        return state in self.states

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node


class QueueFrontier(StackFrontier):

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier.popleft()  # Remoção instantânea O(1)
        self.states.remove(node.state)
        return node
