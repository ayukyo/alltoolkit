# Examples for graph_utils
# Demonstrates common use cases

source("graph_utils.R")

cat("\n=== Graph Utilities Examples ===\n\n")

# Example 1: Social Network Analysis
cat("Example 1: Social Network Analysis\n")
cat("----------------------------------\n")
social <- graph_create(directed = FALSE)
social <- graph_add_edge(social, "Alice", "Bob")
social <- graph_add_edge(social, "Alice", "Charlie")
social <- graph_add_edge(social, "Bob", "David")
social <- graph_add_edge(social, "Charlie", "David")
social <- graph_add_edge(social, "David", "Eve")
social <- graph_add_vertex(social, "Frank")  # Isolated user

graph_print(social)

# Find Alice's network (friends and friends of friends)
cat("\nAlice's network (BFS from Alice):\n")
print(graph_bfs(social, "Alice"))

# Find degrees (popularity)
cat("\nUser degrees (popularity):\n")
print(graph_degree(social))

# Check if everyone is connected
components <- graph_connected_components(social)
cat("\nNumber of separate communities:", length(components), "\n")
for (i in seq_along(components)) {
  cat("Community", i, ":", paste(components[[i]], collapse = ", "), "\n")
}

# Example 2: Road Network - Shortest Path
cat("\n\nExample 2: Road Network - Finding Shortest Route\n")
cat("-------------------------------------------------\n")
roads <- graph_create(directed = FALSE)
roads <- graph_add_edge(roads, "NYC", "Boston", 215)
roads <- graph_add_edge(roads, "NYC", "Philadelphia", 95)
roads <- graph_add_edge(roads, "NYC", "Washington", 225)
roads <- graph_add_edge(roads, "Boston", "Providence", 50)
roads <- graph_add_edge(roads, "Philadelphia", "Washington", 140)
roads <- graph_add_edge(roads, "Philadelphia", "Pittsburgh", 305)
roads <- graph_add_edge(roads, "Washington", "Richmond", 110)
roads <- graph_add_edge(roads, "Pittsburgh", "Cleveland", 135)

cat("\nRoad network vertices:", paste(roads$vertices, collapse = ", "), "\n")
cat("Number of road segments:", nrow(roads$edges), "\n")

# Find shortest path from NYC to Richmond
path <- graph_shortest_path(roads, "NYC", "Richmond")
result <- graph_dijkstra(roads, "NYC")

cat("\nShortest route from NYC to Richmond:\n")
cat("Path:", paste(path, collapse = " -> "), "\n")
cat("Total distance:", result$distances["Richmond"], "miles\n")

# Example 3: Task Dependencies (Topological Sort)
cat("\n\nExample 3: Project Task Scheduling\n")
cat("-----------------------------------\n")
tasks <- graph_create(directed = TRUE)
tasks <- graph_add_edge(tasks, "Design", "Frontend")
tasks <- graph_add_edge(tasks, "Design", "Backend")
tasks <- graph_add_edge(tasks, "Frontend", "Testing")
tasks <- graph_add_edge(tasks, "Backend", "Testing")
tasks <- graph_add_edge(tasks, "Testing", "Deployment")

cat("Task dependencies (DAG):\n")
print(graph_to_edgelist(tasks))

execution_order <- graph_topological_sort(tasks)
cat("\nTask execution order:\n")
for (i in seq_along(execution_order)) {
  cat(i, ".", execution_order[i], "\n")
}

# Example 4: Network Infrastructure - MST
cat("\n\nExample 4: Network Cable Installation (Minimum Spanning Tree)\n")
cat("--------------------------------------------------------------\n")
network <- graph_create(directed = FALSE)
network <- graph_add_edge(network, "Office A", "Office B", 100)
network <- graph_add_edge(network, "Office A", "Office C", 150)
network <- graph_add_edge(network, "Office B", "Office C", 80)
network <- graph_add_edge(network, "Office B", "Office D", 120)
network <- graph_add_edge(network, "Office C", "Office D", 90)

cat("\nAll possible cable routes:\n")
print(graph_to_edgelist(network))

mst <- graph_minimum_spanning_tree(network)
cat("\nOptimal cable routes (MST):\n")
print(mst)
cat("\nTotal cable length:", sum(mst$weight), "meters\n")

# Example 5: Web Crawling Simulation (BFS vs DFS)
cat("\n\nExample 5: Web Crawling Order Comparison\n")
cat("-----------------------------------------\n")
web <- graph_create(directed = FALSE)
web <- graph_add_edge(web, "Home", "About")
web <- graph_add_edge(web, "Home", "Products")
web <- graph_add_edge(web, "Home", "Contact")
web <- graph_add_edge(web, "Products", "Electronics")
web <- graph_add_edge(web, "Products", "Books")
web <- graph_add_edge(web, "Electronics", "Phones")
web <- graph_add_edge(web, "Electronics", "Laptops")

cat("BFS order (level-by-level, good for site maps):\n")
print(graph_bfs(web, "Home"))

cat("\nDFS order (deep-first, good for scraping):\n")
print(graph_dfs(web, "Home"))

# Example 6: Dependency Cycle Detection
cat("\n\nExample 6: Circular Dependency Detection\n")
cat("-----------------------------------------\n")
deps_good <- graph_create(directed = TRUE)
deps_good <- graph_add_edge(deps_good, "A", "B")
deps_good <- graph_add_edge(deps_good, "B", "C")
deps_good <- graph_add_edge(deps_good, "C", "D")

cat("Dependency graph A->B->C->D:\n")
cat("Has cycle?", graph_has_cycle(deps_good), "(expected: FALSE)\n")

deps_bad <- graph_create(directed = TRUE)
deps_bad <- graph_add_edge(deps_bad, "A", "B")
deps_bad <- graph_add_edge(deps_bad, "B", "C")
deps_bad <- graph_add_edge(deps_bad, "C", "A")

cat("\nDependency graph A->B->C->A (circular):\n")
cat("Has cycle?", graph_has_cycle(deps_bad), "(expected: TRUE)\n")

cat("\n=== Examples Complete ===\n")