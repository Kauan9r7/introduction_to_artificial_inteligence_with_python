"""
maze_algorithms.py
Biblioteca contendo as estruturas de dados e funções de busca para solução de labirintos.
"""


class Node:
    """Representa um nó na árvore de busca."""

    def __init__(self, state, parent=None, action=None, cost=0, heuristic=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost          # g(n) -> Custo percorrido
        self.heuristic = heuristic  # h(n) -> Estimativa até o objetivo


class StackFrontier:
    """Fronteira LIFO (Último a entrar, primeiro a sair) -> Usada na Busca em Profundidade (DFS)."""

    def __init__(self):
        self.frontier = []

    def add(self, node):
        self.frontier.append(node)

    def contains_state(self, state):
        return any(node.state == state for node in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[-1]
        self.frontier = self.frontier[:-1]
        return node


class QueueFrontier(StackFrontier):
    """Fronteira FIFO (Primeiro a entrar, primeiro a sair) -> Usada na Busca em Largura (BFS)."""

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        node = self.frontier[0]
        self.frontier = self.frontier[1:]
        return node

class GreedyBestFirstFrontier(StackFrontier):
    """Fronteira para Greedy Best-First Search: escolhe pelo menor h(n)."""
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # Encontra o nó com menor valor de heurística h(n)
        node = min(self.frontier, key=lambda n: n.heuristic)
        self.frontier.remove(node)
        return node


class AStarFrontier(StackFrontier):
    """Fronteira para A* Search: escolhe pelo menor f(n) = g(n) + h(n)."""
    
    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        # Encontra o nó com menor custo total estimado: g(n) + h(n)
        node = min(self.frontier, key=lambda n: n.cost + n.heuristic)
        self.frontier.remove(node)
        return node


def manhattan_distance(state1, state2):
    """Calcula a distância de Manhattan entre duas coordenadas (linha, coluna)."""
    return abs(state1[0] - state2[0]) + abs(state1[1] - state2[1])


def solve_maze_search(start, goal, neighbors_fn, method="dfs"):
    method = method.lower().strip()
    
    if method == "dfs":
        frontier = StackFrontier()
    elif method == "bfs":
        frontier = QueueFrontier()
    elif method == "gbfs":
        frontier = GreedyBestFirstFrontier()
    elif method == "astar":
        frontier = AStarFrontier()
    else:
        raise ValueError(
            f"Método de busca inválido: '{method}'. Utilize 'dfs', 'bfs', 'gbfs' ou 'astar'."
        )

    # 1. Nó inicial:
    # - cost g(n) = 0
    # - heuristic h(n) = distância até o objetivo
    start_heuristic = manhattan_distance(start, goal)
    start_node = Node(
        state=start, 
        parent=None, 
        action=None, 
        cost=0, 
        heuristic=start_heuristic
    )
    frontier.add(start_node)

    explored = set()
    num_explored = 0

    while True:
        if frontier.empty():
            raise Exception("Não há solução para o labirinto.")

        node = frontier.remove()
        num_explored += 1

        if node.state == goal:
            actions = []
            cells = []
            curr = node
            while curr.parent is not None:
                actions.append(curr.action)
                cells.append(curr.state)
                curr = curr.parent
            actions.reverse()
            cells.reverse()
            return (actions, cells), num_explored, explored

        explored.add(node.state)

        # 2. Ao expandir vizinhos:
        for action, state in neighbors_fn(node.state):
            if not frontier.contains_state(state) and state not in explored:
                # Cada passo no labirinto custa +1 em relação ao pai (g(n) = pai.cost + 1)
                child_cost = node.cost + 1
                child_heuristic = manhattan_distance(state, goal)
                
                child = Node(
                    state=state, 
                    parent=node, 
                    action=action, 
                    cost=child_cost, 
                    heuristic=child_heuristic
                )
                frontier.add(child)