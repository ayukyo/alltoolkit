# Graph Utilities for R
# Zero external dependencies - pure R implementation
# Provides graph data structures and common algorithms

#' Create a new graph
#' @param directed Logical, whether the graph is directed (default: FALSE)
#' @return A graph object (list with vertices, edges, and adjacency list)
graph_create <- function(directed = FALSE) {
  list(
    vertices = character(0),
    edges = data.frame(from = character(0), to = character(0), weight = numeric(0), stringsAsFactors = FALSE),
    adjacency = list(),
    directed = directed
  )
}

#' Add a vertex to the graph
#' @param graph The graph object
#' @param vertex The vertex name
#' @return Updated graph object
graph_add_vertex <- function(graph, vertex) {
  if (!(vertex %in% graph$vertices)) {
    graph$vertices <- c(graph$vertices, vertex)
    graph$adjacency[[vertex]] <- list()
  }
  graph
}

#' Add an edge to the graph
#' @param graph The graph object
#' @param from Source vertex
#' @param to Target vertex
#' @param weight Edge weight (default: 1)
#' @return Updated graph object
graph_add_edge <- function(graph, from, to, weight = 1) {
  # Ensure vertices exist
  graph <- graph_add_vertex(graph, from)
  graph <- graph_add_vertex(graph, to)
  
  # Add edge to edges dataframe
  graph$edges <- rbind(graph$edges, data.frame(from = from, to = to, weight = weight, stringsAsFactors = FALSE))
  
  # Update adjacency list
  graph$adjacency[[from]][[to]] <- weight
  
  # For undirected graphs, add reverse edge
  if (!graph$directed) {
    graph$adjacency[[to]][[from]] <- weight
  }
  
  graph
}

#' Get all neighbors of a vertex
#' @param graph The graph object
#' @param vertex The vertex name
#' @return Named numeric vector of neighbors with weights
graph_neighbors <- function(graph, vertex) {
  if (vertex %in% names(graph$adjacency)) {
    unlist(graph$adjacency[[vertex]])
  } else {
    numeric(0)
  }
}

#' Breadth-First Search traversal
#' @param graph The graph object
#' @param start Starting vertex
#' @return Vector of vertices in BFS order
graph_bfs <- function(graph, start) {
  if (!(start %in% graph$vertices)) {
    stop("Start vertex not found in graph")
  }
  
  visited <- character(0)
  queue <- start
  
  while (length(queue) > 0) {
    current <- queue[1]
    queue <- queue[-1]
    
    if (!(current %in% visited)) {
      visited <- c(visited, current)
      neighbors <- names(graph_neighbors(graph, current))
      
      for (neighbor in neighbors) {
        if (!(neighbor %in% visited) && !(neighbor %in% queue)) {
          queue <- c(queue, neighbor)
        }
      }
    }
  }
  
  visited
}

#' Depth-First Search traversal
#' @param graph The graph object
#' @param start Starting vertex
#' @return Vector of vertices in DFS order
graph_dfs <- function(graph, start) {
  if (!(start %in% graph$vertices)) {
    stop("Start vertex not found in graph")
  }
  
  visited <- character(0)
  
  dfs_helper <- function(vertex) {
    if (!(vertex %in% visited)) {
      visited <<- c(visited, vertex)
      neighbors <- names(graph_neighbors(graph, vertex))
      
      for (neighbor in neighbors) {
        if (!(neighbor %in% visited)) {
          dfs_helper(neighbor)
        }
      }
    }
  }
  
  dfs_helper(start)
  visited
}

#' Dijkstra's shortest path algorithm
#' @param graph The graph object
#' @param start Starting vertex
#' @return List with distances and previous vertices
graph_dijkstra <- function(graph, start) {
  if (!(start %in% graph$vertices)) {
    stop("Start vertex not found in graph")
  }
  
  # Initialize distances to infinity
  distances <- setNames(rep(Inf, length(graph$vertices)), graph$vertices)
  distances[start] <- 0
  
  # Previous vertex for path reconstruction
  previous <- setNames(as.list(rep(NA, length(graph$vertices))), graph$vertices)
  
  # Unvisited vertices
  unvisited <- graph$vertices
  
  while (length(unvisited) > 0) {
    # Find vertex with minimum distance
    min_dist <- Inf
    current <- NULL
    
    for (v in unvisited) {
      if (distances[v] < min_dist) {
        min_dist <- distances[v]
        current <- v
      }
    }
    
    if (is.null(current) || min_dist == Inf) break
    
    unvisited <- unvisited[unvisited != current]
    
    # Update neighbors
    neighbors <- graph_neighbors(graph, current)
    
    for (neighbor in names(neighbors)) {
      alt <- distances[current] + neighbors[neighbor]
      if (alt < distances[neighbor]) {
        distances[neighbor] <- alt
        previous[[neighbor]] <- current
      }
    }
  }
  
  list(distances = distances, previous = previous)
}

#' Get shortest path between two vertices
#' @param graph The graph object
#' @param from Starting vertex
#' @param to Ending vertex
#' @return Vector of vertices in path order, or NULL if no path exists
graph_shortest_path <- function(graph, from, to) {
  result <- graph_dijkstra(graph, from)
  
  if (result$distances[to] == Inf) {
    return(NULL)
  }
  
  path <- to
  current <- to
  
  while (!is.na(result$previous[[current]])) {
    current <- result$previous[[current]]
    path <- c(current, path)
  }
  
  path
}

#' Find connected components (for undirected graphs)
#' @param graph The graph object
#' @return List of components, each containing vertex names
graph_connected_components <- function(graph) {
  if (graph$directed) {
    stop("This function is for undirected graphs. Use graph_strongly_connected_components for directed graphs.")
  }
  
  components <- list()
  visited <- character(0)
  
  for (vertex in graph$vertices) {
    if (!(vertex %in% visited)) {
      component <- graph_bfs(graph, vertex)
      components <- c(components, list(component))
      visited <- c(visited, component)
    }
  }
  
  components
}

#' Detect cycle in graph
#' @param graph The graph object
#' @return Logical, TRUE if cycle exists
graph_has_cycle <- function(graph) {
  if (graph$directed) {
    return(graph_has_cycle_directed(graph))
  } else {
    return(graph_has_cycle_undirected(graph))
  }
}

#' Helper for cycle detection in undirected graphs
graph_has_cycle_undirected <- function(graph) {
  visited <- character(0)
  
  dfs_cycle <- function(vertex, parent) {
    visited <<- c(visited, vertex)
    neighbors <- names(graph_neighbors(graph, vertex))
    
    for (neighbor in neighbors) {
      if (!(neighbor %in% visited)) {
        if (dfs_cycle(neighbor, vertex)) {
          return(TRUE)
        }
      } else if (neighbor != parent) {
        return(TRUE)
      }
    }
    return(FALSE)
  }
  
  for (vertex in graph$vertices) {
    if (!(vertex %in% visited)) {
      if (dfs_cycle(vertex, NA)) {
        return(TRUE)
      }
    }
  }
  
  return(FALSE)
}

#' Helper for cycle detection in directed graphs
graph_has_cycle_directed <- function(graph) {
  visited <- character(0)
  rec_stack <- character(0)
  
  dfs_cycle <- function(vertex) {
    visited <<- c(visited, vertex)
    rec_stack <<- c(rec_stack, vertex)
    
    neighbors <- names(graph_neighbors(graph, vertex))
    
    for (neighbor in neighbors) {
      if (!(neighbor %in% visited)) {
        if (dfs_cycle(neighbor)) {
          return(TRUE)
        }
      } else if (neighbor %in% rec_stack) {
        return(TRUE)
      }
    }
    
    rec_stack <<- rec_stack[rec_stack != vertex]
    return(FALSE)
  }
  
  for (vertex in graph$vertices) {
    if (!(vertex %in% visited)) {
      if (dfs_cycle(vertex)) {
        return(TRUE)
      }
    }
  }
  
  return(FALSE)
}

#' Topological sort (for directed acyclic graphs)
#' @param graph The graph object
#' @return Vector of vertices in topological order
graph_topological_sort <- function(graph) {
  if (!graph$directed) {
    stop("Topological sort is only for directed graphs")
  }
  
  if (graph_has_cycle(graph)) {
    stop("Graph contains a cycle, topological sort not possible")
  }
  
  visited <- character(0)
  result <- character(0)
  
  topo_sort <- function(vertex) {
    visited <<- c(visited, vertex)
    neighbors <- names(graph_neighbors(graph, vertex))
    
    for (neighbor in neighbors) {
      if (!(neighbor %in% visited)) {
        topo_sort(neighbor)
      }
    }
    
    result <<- c(vertex, result)
  }
  
  for (vertex in graph$vertices) {
    if (!(vertex %in% visited)) {
      topo_sort(vertex)
    }
  }
  
  result
}

#' Minimum Spanning Tree using Prim's algorithm
#' @param graph The graph object (must be undirected and weighted)
#' @return Data frame of edges in the MST
graph_minimum_spanning_tree <- function(graph) {
  if (graph$directed) {
    stop("MST is only for undirected graphs")
  }
  
  if (length(graph$vertices) == 0) {
    return(data.frame(from = character(0), to = character(0), weight = numeric(0)))
  }
  
  mst_edges <- data.frame(from = character(0), to = character(0), weight = numeric(0))
  in_mst <- character(0)
  
  # Start from first vertex
  current <- graph$vertices[1]
  in_mst <- c(in_mst, current)
  
  while (length(in_mst) < length(graph$vertices)) {
    min_edge <- NULL
    min_weight <- Inf
    
    # Find minimum weight edge from MST to outside
    for (v in in_mst) {
      neighbors <- graph_neighbors(graph, v)
      
      for (neighbor in names(neighbors)) {
        if (!(neighbor %in% in_mst)) {
          if (neighbors[neighbor] < min_weight) {
            min_weight <- neighbors[neighbor]
            min_edge <- c(v, neighbor, neighbors[neighbor])
          }
        }
      }
    }
    
    if (is.null(min_edge)) break
    
    mst_edges <- rbind(mst_edges, data.frame(from = min_edge[1], to = min_edge[2], weight = as.numeric(min_edge[3])))
    in_mst <- c(in_mst, min_edge[2])
  }
  
  mst_edges
}

#' Calculate graph degree (number of edges connected to a vertex)
#' @param graph The graph object
#' @param vertex The vertex name (optional, if NULL returns all degrees)
#' @return Named vector of degrees
graph_degree <- function(graph, vertex = NULL) {
  degrees <- sapply(graph$vertices, function(v) {
    length(graph_neighbors(graph, v))
  })
  
  if (!is.null(vertex)) {
    return(degrees[vertex])
  }
  
  degrees
}

#' Print graph information
#' @param graph The graph object
graph_print <- function(graph) {
  cat("Graph (", ifelse(graph$directed, "directed", "undirected"), ")\n", sep = "")
  cat("Vertices:", length(graph$vertices), "\n")
  cat("Edges:", nrow(graph$edges), "\n")
  cat("Vertices:", paste(graph$vertices, collapse = ", "), "\n")
}

#' Export graph to edge list (useful for visualization)
#' @param graph The graph object
#' @return Data frame with from, to, weight columns
graph_to_edgelist <- function(graph) {
  graph$edges
}

#' Import graph from edge list
#' @param edgelist Data frame with from, to, weight columns
#' @param directed Logical, whether the graph is directed
#' @return Graph object
graph_from_edgelist <- function(edgelist, directed = FALSE) {
  graph <- graph_create(directed = directed)
  
  for (i in 1:nrow(edgelist)) {
    weight <- if ("weight" %in% names(edgelist)) edgelist$weight[i] else 1
    graph <- graph_add_edge(graph, edgelist$from[i], edgelist$to[i], weight)
  }
  
  graph
}