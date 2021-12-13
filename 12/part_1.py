cave_graph = {}
with open('12/input.txt') as f:
    routes = f.read().strip().splitlines()
    for route in routes:
        start, end = route.split('-')
        if start in cave_graph:
            cave_graph[start].add(end)
        else:
            cave_graph[start] = {end}

        if end in cave_graph:
            cave_graph[end].add(start)
        else:
            cave_graph[end] = {start}


def count_paths(graph, node, destination, visited=[], count=0):
    if node == destination:
        return 1
    else:
        visited.append(node)
        for n in graph[node]:
            if n in visited and n.islower():
                continue
            else:
                count += count_paths(graph=graph, node=n,
                                     destination=destination, visited=visited.copy())
        return count


total = count_paths(graph=cave_graph, node='start',
                    destination='end')

print(total)
