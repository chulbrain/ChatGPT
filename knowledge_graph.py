class KnowledgeGraph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, subject, relation, obj):
        if subject not in self.graph:
            self.graph[subject] = []
        self.graph[subject].append((relation, obj))

    def get_relations(self, subject):
        return self.graph.get(subject, [])

    def _bfs(self, start, end, max_depth):
        from collections import deque
        queue = deque([(start, [start])])
        visited = {start}
        while queue:
            node, path = queue.popleft()
            if node == end:
                return path
            if len(path) > max_depth:
                continue
            for _, neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def find_path(self, start, end, max_depth=3):
        return self._bfs(start, end, max_depth)

    @classmethod
    def from_csv(cls, path):
        import csv
        kg = cls()
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for subject, relation, obj in reader:
                kg.add_edge(subject, relation, obj)
        return kg

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Simple Knowledge Graph")
    parser.add_argument('--data', default='sample_data.csv', help='CSV file with subject,relation,object columns')
    parser.add_argument('--path', nargs=2, metavar=('START', 'END'), help='find path from START to END')
    args = parser.parse_args()

    kg = KnowledgeGraph.from_csv(args.data)
    if args.path:
        start, end = args.path
        path = kg.find_path(start, end)
        if path:
            print(' -> '.join(path))
        else:
            print(f'No path found from {start} to {end}')
    else:
        for subject, relations in kg.graph.items():
            for relation, obj in relations:
                print(f"{subject} --{relation}--> {obj}")
