import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.LinkedList;
import java.util.Queue;
import java.util.HashSet;
import java.util.HashMap;
import java.util.PriorityQueue;

/**
 * Your implementation of various different graph algorithms.
 *
 * @author Jinseo Lee
 * @userid jlee4223
 * @GTID 903950086
 * @version 1.0
 */
public class GraphAlgorithms {

    /**
     * Performs a breadth first search (bfs) on the input graph, starting at
     * the parameterized starting vertex.
     * <p>
     * When exploring a vertex, explore in the order of neighbors returned by
     * the adjacency list. Failure to do so may cause you to lose points.
     * <p>
     * You may import/use java.util.Set, java.util.List, java.util.Queue, and
     * any classes that implement the aforementioned interfaces, as long as they
     * are efficient.
     * <p>
     * The only instance of java.util.Map that you may use is the
     * adjacency list from graph. DO NOT create new instances of Map
     * for BFS (storing the adjacency list in a variable is fine).
     * <p>
     * DO NOT modify the structure of the graph. The graph should be unmodified
     * after this method terminates.
     *
     * @param <T>   the generic typing of the data
     * @param start the vertex to begin the bfs on
     * @param graph the graph to search through
     * @return list of vertices in visited order
     * @throws IllegalArgumentException if any input is null, or if start
     *                                  doesn't exist in the graph
     */
    public static <T> List<Vertex<T>> bfs(Vertex<T> start, Graph<T> graph) {
        if (start == null || graph == null || !graph.getVertices().contains(start)) {
            throw new IllegalArgumentException("Invalid input / start not in the graph");
        }
        List<Vertex<T>> visited = new ArrayList<>();
        Queue<Vertex<T>> q = new LinkedList<>();
        Set<Vertex<T>> visitedSet = new HashSet<>();

        visitedSet.add(start);
        q.add(start);
        while (!q.isEmpty() && visited.size() < graph.getVertices().size()) {
            Vertex<T> current = q.remove();
            visited.add(current);
            for (VertexDistance<T> neighbor : graph.getAdjList().get(current)) {
                Vertex<T> next = neighbor.getVertex();
                if (!visitedSet.contains(next)) {
                    q.add(next);
                    visitedSet.add(next);
                }
            }
        }
        return visited;
    }

    /**
     * Performs a depth first search (dfs) on the input graph, starting at
     * the parameterized starting vertex.
     * <p>
     * When exploring a vertex, explore in the order of neighbors returned by
     * the adjacency list. Failure to do so may cause you to lose points.
     * <p>
     * *NOTE* You MUST implement this method recursively, or else you will lose
     * all points for this method.
     * <p>
     * You may import/use java.util.Set, java.util.List, and
     * any classes that implement the aforementioned interfaces, as long as they
     * are efficient.
     * <p>
     * The only instance of java.util.Map that you may use is the
     * adjacency list from graph. DO NOT create new instances of Map
     * for DFS (storing the adjacency list in a variable is fine).
     * <p>
     * DO NOT modify the structure of the graph. The graph should be unmodified
     * after this method terminates.
     *
     * @param <T>   the generic typing of the data
     * @param start the vertex to begin the dfs on
     * @param graph the graph to search through
     * @return list of vertices in visited order
     * @throws IllegalArgumentException if any input is null, or if start
     *                                  doesn't exist in the graph
     */
    public static <T> List<Vertex<T>> dfs(Vertex<T> start, Graph<T> graph) {
        if (start == null || graph == null || !graph.getVertices().contains(start)) {
            throw new IllegalArgumentException("Invalid input / start not in the graph");
        }
        List<Vertex<T>> visited = new ArrayList<>();
        Set<Vertex<T>> visitedSet = new HashSet<>();
        dfsRecursive(start, graph, visited, visitedSet);

        return visited;
    }

    private static <T> void dfsRecursive(Vertex<T> current, Graph<T> graph, List<Vertex<T>> visited,
                                         Set<Vertex<T>> visitedSet) {
        visited.add(current);
        visitedSet.add(current);

        for (VertexDistance<T> neighbor : graph.getAdjList().get(current)) {
            Vertex<T> next = neighbor.getVertex();
            if (!visitedSet.contains(next)) {
                dfsRecursive(next, graph, visited, visitedSet);
            }
        }
    }

    /**
     * Finds the single-source shortest distance between the start vertex and
     * all vertices given a weighted graph (you may assume non-negative edge
     * weights).
     * <p>
     * Return a map of the shortest distances such that the key of each entry
     * is a node in the graph and the value for the key is the shortest distance
     * to that node from start, or Integer.MAX_VALUE (representing
     * infinity) if no path exists.
     * <p>
     * You may import/use java.util.PriorityQueue,
     * java.util.Map, and java.util.Set and any class that
     * implements the aforementioned interfaces, as long as your use of it
     * is efficient as possible.
     * <p>
     * You should implement the version of Dijkstra's where you use two
     * termination conditions in conjunction.
     * <p>
     * 1) Check if all of the vertices have been visited.
     * 2) Check if the PQ is empty.
     * <p>
     * DO NOT modify the structure of the graph. The graph should be unmodified
     * after this method terminates.
     *
     * @param <T>   the generic typing of the data
     * @param start the vertex to begin the Dijkstra's on (source)
     * @param graph the graph we are applying Dijkstra's to
     * @return a map of the shortest distances from start to every
     * other node in the graph
     * @throws IllegalArgumentException if any input is null, or if start
     *                                  doesn't exist in the graph.
     */
    public static <T> Map<Vertex<T>, Integer> dijkstras(Vertex<T> start,
                                                        Graph<T> graph) {
        if (start == null || graph == null || !graph.getVertices().contains(start)) {
            throw new IllegalArgumentException("Invalid input / start not in the graph");
        }
        Map<Vertex<T>, Integer> distances = new HashMap<>();
        Set<Vertex<T>> visited = new HashSet<>();
        PriorityQueue<VertexDistance<T>> pq = new PriorityQueue<>();

        for (Vertex<T> vertex : graph.getVertices()) {
            distances.put(vertex, Integer.MAX_VALUE);
        }
        distances.put(start, 0);
        pq.add(new VertexDistance<>(start, 0));

        while (!pq.isEmpty() && visited.size() < graph.getVertices().size()) {
            VertexDistance<T> current = pq.remove();
            Vertex<T> currentVertex = current.getVertex();
            if (!visited.contains(currentVertex)) {
                visited.add(currentVertex);
                for (VertexDistance<T> neighbor : graph.getAdjList().get(currentVertex)) {
                    Vertex<T> next = neighbor.getVertex();
                    int newDistance = distances.get(currentVertex) + neighbor.getDistance();
                    if (newDistance < distances.get(next)) {
                        distances.put(next, newDistance);
                        pq.add(new VertexDistance<>(next, newDistance));
                    }
                }
            }
        }
        return distances;
    }

    /**
     * Runs Prim's algorithm on the given graph and returns the Minimum
     * Spanning Tree (MST) in the form of a set of Edges. If the graph is
     * disconnected and therefore no valid MST exists, return null.
     * <p>
     * You may assume that the passed in graph is undirected. In this framework,
     * this means that if (u, v, 3) is in the graph, then the opposite edge
     * (v, u, 3) will also be in the graph, though as a separate Edge object.
     * <p>
     * The returned set of edges should form an undirected graph. This means
     * that every time you add an edge to your return set, you should add the
     * reverse edge to the set as well. This is for testing purposes. This
     * reverse edge does not need to be the one from the graph itself; you can
     * just make a new edge object representing the reverse edge.
     * <p>
     * You may assume that there will only be one valid MST that can be formed.
     * <p>
     * You should NOT allow self-loops or parallel edges in the MST.
     * <p>
     * You may import/use PriorityQueue, java.util.Set, and any class that
     * implements the aforementioned interface.
     * <p>
     * DO NOT modify the structure of the graph. The graph should be unmodified
     * after this method terminates.
     * <p>
     * The only instance of java.util.Map that you may use is the
     * adjacency list from graph. DO NOT create new instances of Map
     * for this method (storing the adjacency list in a variable is fine).
     *
     * @param <T>   the generic typing of the data
     * @param start the vertex to begin Prims on
     * @param graph the graph we are applying Prims to
     * @return the MST of the graph or null if there is no valid MST
     * @throws IllegalArgumentException if any input is null, or if start
     *                                  doesn't exist in the graph.
     */
    public static <T> Set<Edge<T>> prims(Vertex<T> start, Graph<T> graph) {
        if (start == null || graph == null || !graph.getVertices().contains(start)) {
            throw new IllegalArgumentException("Invalid input / start not in the graph");
        }

        Set<Edge<T>> mst = new HashSet<>();
        Set<Vertex<T>> visited = new HashSet<>();
        PriorityQueue<Edge<T>> pq = new PriorityQueue<>();

        visited.add(start);
        for (VertexDistance<T> neighbor : graph.getAdjList().get(start)) {
            Vertex<T> next = neighbor.getVertex();
            if (!visited.contains(next)) {
                pq.add(new Edge<>(start, next, neighbor.getDistance()));
            }
        }

        while (!pq.isEmpty() && visited.size() < graph.getVertices().size()) {
            Edge<T> edge = pq.remove();
            Vertex<T> u = edge.getU();
            Vertex<T> v = edge.getV();

            if (!(visited.contains(u) && visited.contains(v))) {
                mst.add(edge);
                Edge<T> revEdge = new Edge<>(v, u, edge.getWeight());
                mst.add(revEdge);
                visited.add(v);

                for (VertexDistance<T> neighbor : graph.getAdjList().get(v)) {
                    Vertex<T> next = neighbor.getVertex();
                    if (!visited.contains(next)) {
                        pq.add(new Edge<>(v, next, neighbor.getDistance()));
                    }
                }
            }
        }
        return visited.size() == graph.getVertices().size() ? mst : null;
    }
}
