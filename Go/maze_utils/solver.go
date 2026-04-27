package maze_utils

import (
	"container/heap"
)

// SolveBFS 使用广度优先搜索求解迷宫
// 特点：保证最短路径
func SolveBFS(m *Maze, start, end [2]int) Path {
	if start == [2]int{-1, -1} {
		start = m.Start
	}
	if end == [2]int{-1, -1} {
		end = m.End
	}

	// BFS 队列
	queue := [][2]int{start}
	visited := make(map[[2]int]bool)
	parent := make(map[[2]int][2]int)

	visited[start] = true
	parent[start] = [2]int{-1, -1}

	for len(queue) > 0 {
		current := queue[0]
		queue = queue[1:]

		if current == end {
			// 重建路径
			return reconstructPath(parent, end)
		}

		for _, neighbor := range m.GetPassages(current[0], current[1]) {
			if !visited[neighbor] {
				visited[neighbor] = true
				parent[neighbor] = current
				queue = append(queue, neighbor)
			}
		}
	}

	return nil // 无解
}

// SolveDFS 使用深度优先搜索求解迷宫
// 特点：快速找到任意路径，但不保证最短
func SolveDFS(m *Maze, start, end [2]int) Path {
	if start == [2]int{-1, -1} {
		start = m.Start
	}
	if end == [2]int{-1, -1} {
		end = m.End
	}

	visited := make(map[[2]int]bool)
	path := make(Path, 0)

	var dfs func(current [2]int) bool
	dfs = func(current [2]int) bool {
		if current == end {
			path = append(path, current)
			return true
		}

		visited[current] = true
		path = append(path, current)

		for _, neighbor := range m.GetPassages(current[0], current[1]) {
			if !visited[neighbor] {
				if dfs(neighbor) {
					return true
				}
			}
		}

		// 回溯
		path = path[:len(path)-1]
		return false
	}

	if dfs(start) {
		return path
	}
	return nil
}

// SolveAStar 使用 A* 算法求解迷宫
// 特点：启发式最短路径
func SolveAStar(m *Maze, start, end [2]int) Path {
	if start == [2]int{-1, -1} {
		start = m.Start
	}
	if end == [2]int{-1, -1} {
		end = m.End
	}

	// 曼哈顿距离启发函数
	heuristic := func(pos [2]int) int {
		return abs(pos[0]-end[0]) + abs(pos[1]-end[1])
	}

	// 优先队列
	pq := &priorityQueue{}
	heap.Init(pq)

	// gScore: 从起点到当前节点的实际距离
	gScore := make(map[[2]int]int)
	gScore[start] = 0

	// fScore: gScore + 启发值
	fScore := make(map[[2]int]int)
	fScore[start] = heuristic(start)

	// 父节点
	parent := make(map[[2]int][2]int)

	// 将起点加入队列
	heap.Push(pq, &node{pos: start, fScore: fScore[start]})

	for pq.Len() > 0 {
		current := heap.Pop(pq).(*node).pos

		if current == end {
			return reconstructPath(parent, end)
		}

		for _, neighbor := range m.GetPassages(current[0], current[1]) {
			tentativeGScore := gScore[current] + 1

			if g, exists := gScore[neighbor]; !exists || tentativeGScore < g {
				parent[neighbor] = current
				gScore[neighbor] = tentativeGScore
				fScore[neighbor] = tentativeGScore + heuristic(neighbor)
				heap.Push(pq, &node{pos: neighbor, fScore: fScore[neighbor]})
			}
		}
	}

	return nil
}

// SolveWallFollower 使用墙跟随算法求解迷宫
// 特点：简单有效，适合完美迷宫
// hand: "left" 或 "right"，决定跟随左手墙还是右手墙
func SolveWallFollower(m *Maze, start, end [2]int, hand string) Path {
	if start == [2]int{-1, -1} {
		start = m.Start
	}
	if end == [2]int{-1, -1} {
		end = m.End
	}

	path := make(Path, 0)
	current := start
	visited := make(map[[2]int]bool)

	// 方向: 北、东、南、西
	// 北=0, 东=1, 南=2, 西=3
	direction := North

	// 获取方向偏移
	dirOffset := map[Direction][2]int{
		North: {0, -1},
		East:  {1, 0},
		South: {0, 1},
		West:  {-1, 0},
	}

	maxSteps := m.Width * m.Height * 4
	steps := 0

	for current != end && steps < maxSteps {
		steps++
		if !visited[current] {
			path = append(path, current)
			visited[current] = true
		}

		cell, _ := m.GetCell(current[0], current[1])

		// 尝试按照墙跟随规则移动
		// 优先尝试转向，然后直行，最后后退
		tryDirs := []Direction{
			Direction((int(direction) + 3) % 4), // 左转
			direction,                           // 直行
			Direction((int(direction) + 1) % 4), // 右转
			Direction((int(direction) + 2) % 4), // 后退
		}

		if hand == "right" {
			tryDirs = []Direction{
				Direction((int(direction) + 1) % 4), // 右转
				direction,                           // 直行
				Direction((int(direction) + 3) % 4), // 左转
				Direction((int(direction) + 2) % 4), // 后退
			}
		}

		moved := false
		for _, tryDir := range tryDirs {
			if !cell.HasWall(tryDir) {
				offset := dirOffset[tryDir]
				nx, ny := current[0]+offset[0], current[1]+offset[1]
				if nx >= 0 && nx < m.Width && ny >= 0 && ny < m.Height {
					current = [2]int{nx, ny}
					direction = tryDir
					moved = true
					break
				}
			}
		}

		if !moved {
			// 无法移动，回溯
			if len(path) > 0 {
				path = path[:len(path)-1]
				if len(path) > 0 {
					current = path[len(path)-1]
				} else {
					break
				}
			}
		}
	}

	if current == end {
		path = append(path, end)
		return path
	}
	return nil
}

// SolveDeadEndFilling 使用死胡同填充算法求解迷宫
// 特点：系统性消除死路
func SolveDeadEndFilling(m *Maze, start, end [2]int) Path {
	if start == [2]int{-1, -1} {
		start = m.Start
	}
	if end == [2]int{-1, -1} {
		end = m.End
	}

	// 创建迷宫副本
	mazeCopy := m.Copy()

	// 找到所有死胡同
	findDeadEnds := func() [][2]int {
		var ends [][2]int
		for y := 0; y < mazeCopy.Height; y++ {
			for x := 0; x < mazeCopy.Width; x++ {
				pos := [2]int{x, y}
				if pos == start || pos == end {
					continue
				}
				passages := mazeCopy.GetPassages(x, y)
				if len(passages) == 1 {
					ends = append(ends, pos)
				}
			}
		}
		return ends
	}

	// 填充死胡同
	for {
		deadEnds := findDeadEnds()
		if len(deadEnds) == 0 {
			break
		}

		for _, deadEnd := range deadEnds {
			x, y := deadEnd[0], deadEnd[1]
			passages := mazeCopy.GetPassages(x, y)
			if len(passages) == 1 {
				// 封闭这个单元格
				neighbor := passages[0]
				mazeCopy.AddWall(x, y, neighbor[0], neighbor[1])
			}
		}
	}

	// 在处理后的迷宫上运行 BFS
	return SolveBFS(mazeCopy, start, end)
}

// reconstructPath 从父节点映射重建路径
func reconstructPath(parent map[[2]int][2]int, end [2]int) Path {
	path := make(Path, 0)
	current := end

	for current != [2]int{-1, -1} {
		path = append([][2]int{current}, path...)
		p, exists := parent[current]
		if !exists {
			break
		}
		current = p
	}

	return path
}

// 优先队列实现（用于 A* 算法）
type node struct {
	pos    [2]int
	fScore int
	index  int
}

type priorityQueue []*node

func (pq priorityQueue) Len() int { return len(pq) }

func (pq priorityQueue) Less(i, j int) bool {
	return pq[i].fScore < pq[j].fScore
}

func (pq priorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priorityQueue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*node)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priorityQueue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil
	item.index = -1
	*pq = old[0 : n-1]
	return item
}