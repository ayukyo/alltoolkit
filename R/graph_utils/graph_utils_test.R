# Test file for graph_utils
# Run with: Rscript graph_utils_test.R

source("graph_utils.R")

test_that <- function(description, expr) {
  tryCatch({
    result <- eval(expr)
    if (isTRUE(result)) {
      cat("✓ PASS:", description, "\n")
    } else {
      cat("✗ FAIL:", description, "- Expected TRUE, got", result, "\n")
    }
  }, error = function(e) {
    cat("✗ ERROR:", description, "-", e$message, "\n")
  })
}

cat("\n=== Graph Utilities Test Suite ===\n\n")

# Test 1: Create graph
cat("--- Test: Graph Creation ---\n")
g <- graph_create(directed = FALSE)
test_that("Creates empty graph", length(g$vertices) == 0)
test_that("Empty graph has no edges", nrow(g$edges) == 0)

# Test 2: Add vertices
cat("\n--- Test: Vertex Operations ---\n")
g <- graph_add_vertex(g, "A")
g <- graph_add_vertex(g, "B")
g <- graph_add_vertex(g, "C")
test_that("Adds vertices correctly", length(g$vertices) == 3)
test_that("Vertices are stored correctly", all(c("A", "B", "C") %in% g$vertices))

# Test 3: Add edges
cat("\n--- Test: Edge Operations ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B", 5)
g <- graph_add_edge(g, "B", "C", 3)
g <- graph_add_edge(g, "A", "C", 10)
test_that("Edges are added correctly", nrow(g$edges) == 3)
test_that("Vertices auto-created from edges", length(g$vertices) == 3)

# Test 4: BFS
cat("\n--- Test: BFS Traversal ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B")
g <- graph_add_edge(g, "A", "C")
g <- graph_add_edge(g, "B", "D")
g <- graph_add_edge(g, "C", "E")
bfs_result <- graph_bfs(g, "A")
test_that("BFS starts from A", bfs_result[1] == "A")
test_that("BFS visits all vertices", length(bfs_result) == 5)

# Test 5: DFS
cat("\n--- Test: DFS Traversal ---\n")
dfs_result <- graph_dfs(g, "A")
test_that("DFS starts from A", dfs_result[1] == "A")
test_that("DFS visits all vertices", length(dfs_result) == 5)

# Test 6: Dijkstra
cat("\n--- Test: Dijkstra's Algorithm ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B", 4)
g <- graph_add_edge(g, "A", "C", 2)
g <- graph_add_edge(g, "B", "C", 1)
g <- graph_add_edge(g, "B", "D", 5)
g <- graph_add_edge(g, "C", "D", 8)

result <- graph_dijkstra(g, "A")
test_that("Distance to A is 0", result$distances["A"] == 0)
test_that("Distance to C is 2", result$distances["C"] == 2)
test_that("Distance to B is 3 (A->C->B)", result$distances["B"] == 3)
test_that("Distance to D is 8 (A->C->B->D)", result$distances["D"] == 8)

# Test 7: Shortest path
cat("\n--- Test: Shortest Path ---\n")
path <- graph_shortest_path(g, "A", "D")
test_that("Path starts from A", path[1] == "A")
test_that("Path ends at D", path[length(path)] == "D")
test_that("Path length is correct", length(path) == 4)

# Test 8: Connected components
cat("\n--- Test: Connected Components ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B")
g <- graph_add_edge(g, "B", "C")
g <- graph_add_edge(g, "D", "E")
g <- graph_add_vertex(g, "F")  # Isolated vertex

components <- graph_connected_components(g)
test_that("Three components exist", length(components) == 3)

# Test 9: Cycle detection (undirected)
cat("\n--- Test: Cycle Detection (Undirected) ---\n")
# Graph with cycle
g_cycle <- graph_create(directed = FALSE)
g_cycle <- graph_add_edge(g_cycle, "A", "B")
g_cycle <- graph_add_edge(g_cycle, "B", "C")
g_cycle <- graph_add_edge(g_cycle, "C", "A")
test_that("Detects cycle in triangle graph", graph_has_cycle(g_cycle) == TRUE)

# Graph without cycle (tree)
g_tree <- graph_create(directed = FALSE)
g_tree <- graph_add_edge(g_tree, "A", "B")
g_tree <- graph_add_edge(g_tree, "A", "C")
g_tree <- graph_add_edge(g_tree, "B", "D")
test_that("No cycle in tree graph", graph_has_cycle(g_tree) == FALSE)

# Test 10: Cycle detection (directed)
cat("\n--- Test: Cycle Detection (Directed) ---\n")
g_dir <- graph_create(directed = TRUE)
g_dir <- graph_add_edge(g_dir, "A", "B")
g_dir <- graph_add_edge(g_dir, "B", "C")
g_dir <- graph_add_edge(g_dir, "C", "A")
test_that("Detects cycle in directed graph", graph_has_cycle(g_dir) == TRUE)

g_dag <- graph_create(directed = TRUE)
g_dag <- graph_add_edge(g_dag, "A", "B")
g_dag <- graph_add_edge(g_dag, "B", "C")
test_that("No cycle in DAG", graph_has_cycle(g_dag) == FALSE)

# Test 11: Topological sort
cat("\n--- Test: Topological Sort ---\n")
g_dag <- graph_create(directed = TRUE)
g_dag <- graph_add_edge(g_dag, "A", "B")
g_dag <- graph_add_edge(g_dag, "A", "C")
g_dag <- graph_add_edge(g_dag, "B", "D")
g_dag <- graph_add_edge(g_dag, "C", "D")

topo <- graph_topological_sort(g_dag)
test_that("Topological sort has correct length", length(topo) == 4)
test_that("A comes before B in topological order", which(topo == "A") < which(topo == "B"))
test_that("A comes before C in topological order", which(topo == "A") < which(topo == "C"))
test_that("B and C come before D", which(topo == "D") > which(topo == "B") && which(topo == "D") > which(topo == "C"))

# Test 12: Minimum Spanning Tree
cat("\n--- Test: Minimum Spanning Tree ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B", 4)
g <- graph_add_edge(g, "A", "C", 3)
g <- graph_add_edge(g, "B", "C", 1)
g <- graph_add_edge(g, "B", "D", 2)
g <- graph_add_edge(g, "C", "D", 5)

mst <- graph_minimum_spanning_tree(g)
total_weight <- sum(mst$weight)
test_that("MST has n-1 edges for n vertices", nrow(mst) == 3)
test_that("MST total weight is minimal", total_weight == 6) # B-C(1) + B-D(2) + A-C(3)

# Test 13: Graph degree
cat("\n--- Test: Graph Degree ---\n")
g <- graph_create(directed = FALSE)
g <- graph_add_edge(g, "A", "B")
g <- graph_add_edge(g, "A", "C")
g <- graph_add_edge(g, "B", "C")

degrees <- graph_degree(g)
test_that("Degree of A is 2", degrees["A"] == 2)
test_that("Degree of B is 2", degrees["B"] == 2)
test_that("Degree of C is 2", degrees["C"] == 2)
test_that("Single vertex degree works", graph_degree(g, "A") == 2)

# Test 14: Export/Import
cat("\n--- Test: Export/Import Edge List ---\n")
g_orig <- graph_create(directed = FALSE)
g_orig <- graph_add_edge(g_orig, "A", "B", 10)
g_orig <- graph_add_edge(g_orig, "B", "C", 20)

edgelist <- graph_to_edgelist(g_orig)
test_that("Export creates correct edge list", nrow(edgelist) == 2)

g_import <- graph_from_edgelist(edgelist, directed = FALSE)
test_that("Import recreates vertices", length(g_import$vertices) == 3)
test_that("Import recreates edges", nrow(g_import$edges) == 2)

# Test 15: Directed graph behavior
cat("\n--- Test: Directed Graph Behavior ---\n")
g_dir <- graph_create(directed = TRUE)
g_dir <- graph_add_edge(g_dir, "A", "B", 5)
test_that("Directed graph has correct adjacency", "B" %in% names(g_dir$adjacency[["A"]]))
test_that("Directed graph reverse edge not added", !("A" %in% names(g_dir$adjacency[["B"]])))

cat("\n=== All Tests Completed ===\n")