"""
Module 3: Route Optimization
Algorithm: Dijkstra's Shortest Path + Nearest Neighbor heuristic for TSP
"""
import math
import heapq


def _haversine_distance(lat1, lng1, lat2, lng2):
    """Calculate distance in km between two coordinates using Haversine formula."""
    R = 6371  # Earth radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _build_distance_graph(places):
    """Build complete undirected distance graph between all places."""
    n = len(places)
    graph = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                graph[i][j] = _haversine_distance(
                    places[i]['lat'], places[i]['lng'],
                    places[j]['lat'], places[j]['lng']
                )
    return graph


def dijkstra(graph, start):
    """
    Dijkstra's algorithm to find shortest distances from start node.
    Returns: (distances dict, predecessors dict)
    """
    n = len(graph)
    dist = [float('inf')] * n
    dist[start] = 0
    prev = [-1] * n
    visited = [False] * n
    pq = [(0, start)]

    while pq:
        d, u = heapq.heappop(pq)
        if visited[u]:
            continue
        visited[u] = True
        for v in range(n):
            if not visited[v] and graph[u][v] > 0:
                new_dist = dist[u] + graph[u][v]
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    prev[v] = u
                    heapq.heappush(pq, (new_dist, v))

    return dist, prev


def _nearest_neighbor_tour(graph, start=0):
    """
    Nearest neighbor heuristic for TSP.
    Builds a tour starting from 'start' by always visiting the closest unvisited node.
    """
    n = len(graph)
    visited = [False] * n
    tour = [start]
    visited[start] = True
    total_dist = 0.0

    current = start
    for _ in range(n - 1):
        best_dist = float('inf')
        best_next = -1
        for j in range(n):
            if not visited[j] and graph[current][j] < best_dist:
                best_dist = graph[current][j]
                best_next = j
        if best_next == -1:
            break
        tour.append(best_next)
        visited[best_next] = True
        total_dist += best_dist
        current = best_next

    return tour, total_dist


def optimize_route(places):
    """
    Optimize visiting order of attractions using Dijkstra + Nearest Neighbor heuristic.

    Input: list of {name, lat, lng, ...}
    Output: {
        ordered_places: [...],
        total_distance_km: float,
        segments: [{from, to, distance_km}],
        dijkstra_distances: {name: shortest_from_first}
    }
    """
    if not places or len(places) < 2:
        return {
            'ordered_places': places,
            'total_distance_km': 0,
            'segments': [],
            'dijkstra_distances': {}
        }

    graph = _build_distance_graph(places)
    n = len(places)

    # Run Dijkstra from the first place (hotel/base)
    dijk_dist, _ = dijkstra(graph, 0)

    # Use nearest-neighbor heuristic for full tour order
    tour_indices, total_dist = _nearest_neighbor_tour(graph, start=0)

    ordered = [places[i] for i in tour_indices]

    # Build segments
    segments = []
    for k in range(len(tour_indices) - 1):
        i, j = tour_indices[k], tour_indices[k + 1]
        segments.append({
            'from': places[i]['name'],
            'to': places[j]['name'],
            'distance_km': round(graph[i][j], 2),
            'travel_time_min': round(graph[i][j] / 30 * 60, 0)  # assume 30 km/h avg
        })

    return {
        'ordered_places': ordered,
        'total_distance_km': round(total_dist, 2),
        'segments': segments,
        'dijkstra_distances': {places[i]['name']: round(dijk_dist[i], 2) for i in range(n)}
    }
