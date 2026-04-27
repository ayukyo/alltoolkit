package maze_utils

import (
	"math/rand"
	"sort"
	"time"
)

// 生成器配置
type GeneratorConfig struct {
	Seed int64
}

// initRandom 初始化随机数生成器
func initRandom(seed int64) *rand.Rand {
	if seed == 0 {
		seed = time.Now().UnixNano()
	}
	return rand.New(rand.NewSource(seed))
}

// GenerateDFS 使用深度优先搜索算法生成迷宫
// 特点：生成长廊，路径曲折
func GenerateDFS(width, height int, seed int64) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	visited := make(map[[2]int]bool)
	var stack [][2]int

	// 从起点开始
	start := [2]int{0, 0}
	stack = append(stack, start)
	visited[start] = true

	for len(stack) > 0 {
		current := stack[len(stack)-1]
		x, y := current[0], current[1]

		// 获取未访问的邻居
		neighbors := getUnvisitedNeighbors(m, x, y, visited)
		if len(neighbors) == 0 {
			stack = stack[:len(stack)-1]
			continue
		}

		// 随机选择一个邻居
		next := neighbors[r.Intn(len(neighbors))]
		nx, ny := next[0], next[1]

		// 移除墙
		m.RemoveWall(x, y, nx, ny)

		// 标记为已访问
		visited[next] = true
		stack = append(stack, next)
	}

	return m
}

// GeneratePrim 使用 Prim 算法生成迷宫
// 特点：均匀分布，分支多
func GeneratePrim(width, height int, seed int64) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	inMaze := make(map[[2]int]bool)
	walls := make([][4]int, 0) // [x1, y1, x2, y2]

	// 从起点开始
	start := [2]int{0, 0}
	inMaze[start] = true

	// 添加起点的所有墙
	walls = addWalls(m, 0, 0, walls)

	for len(walls) > 0 {
		// 随机选择一面墙
		idx := r.Intn(len(walls))
		wall := walls[idx]
		walls = append(walls[:idx], walls[idx+1:]...)

		x1, y1, x2, y2 := wall[0], wall[1], wall[2], wall[3]
		cell1 := [2]int{x1, y1}
		cell2 := [2]int{x2, y2}

		// 如果只有一个单元格在迷宫中
		if inMaze[cell1] != inMaze[cell2] {
			// 移除墙
			m.RemoveWall(x1, y1, x2, y2)

			// 将新单元格加入迷宫
			if !inMaze[cell1] {
				inMaze[cell1] = true
				walls = addWalls(m, x1, y1, walls)
			}
			if !inMaze[cell2] {
				inMaze[cell2] = true
				walls = addWalls(m, x2, y2, walls)
			}
		}
	}

	return m
}

// GenerateKruskal 使用 Kruskal 算法生成迷宫
// 特点：无偏差的均匀迷宫
func GenerateKruskal(width, height int, seed int64) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	// 创建并查集
	parent := make(map[[2]int][2]int)
	rank := make(map[[2]int]int)

	// 初始化每个单元格
	cells := make([][2]int, 0)
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			cell := [2]int{x, y}
			parent[cell] = cell
			rank[cell] = 0
			cells = append(cells, cell)
		}
	}

	// 查找函数 - 使用闭包前的变量声明以支持递归
	var find func([2]int) [2]int
	find = func(cell [2]int) [2]int {
		if parent[cell] != cell {
			parent[cell] = find(parent[cell])
		}
		return parent[cell]
	}

	// 合并函数
	union := func(cell1, cell2 [2]int) bool {
		root1 := find(cell1)
		root2 := find(cell2)
		if root1 == root2 {
			return false
		}
		if rank[root1] < rank[root2] {
			parent[root1] = root2
		} else if rank[root1] > rank[root2] {
			parent[root2] = root1
		} else {
			parent[root2] = root1
			rank[root1]++
		}
		return true
	}

	// 创建所有可能的墙（边）
	type edge struct {
		x1, y1, x2, y2 int
	}
	edges := make([]edge, 0)
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			if x < width-1 {
				edges = append(edges, edge{x, y, x + 1, y})
			}
			if y < height-1 {
				edges = append(edges, edge{x, y, x, y + 1})
			}
		}
	}

	// 随机打乱边
	r.Shuffle(len(edges), func(i, j int) {
		edges[i], edges[j] = edges[j], edges[i]
	})

	// 处理每条边
	for _, e := range edges {
		cell1 := [2]int{e.x1, e.y1}
		cell2 := [2]int{e.x2, e.y2}
		if union(cell1, cell2) {
			m.RemoveWall(e.x1, e.y1, e.x2, e.y2)
		}
	}

	return m
}

// GenerateRecursiveDivision 使用递归分割算法生成迷宫
// 特点：先建房间再分割，长直走廊
func GenerateRecursiveDivision(width, height int, seed int64) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	// 首先移除所有内部墙
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			if x < width-1 {
				m.RemoveWall(x, y, x+1, y)
			}
			if y < height-1 {
				m.RemoveWall(x, y, x, y+1)
			}
		}
	}

	// 递归分割
	divide(m, r, 0, 0, width, height, chooseOrientation(width, height, r))

	return m
}

// chooseOrientation 选择分割方向
func chooseOrientation(width, height int, r *rand.Rand) bool {
	// true = 水平分割, false = 垂直分割
	if width < height {
		return true
	} else if height < width {
		return false
	}
	return r.Intn(2) == 0
}

// divide 递归分割
func divide(m *Maze, r *rand.Rand, x, y, width, height int, horizontal bool) {
	if width < 2 || height < 2 {
		return
	}

	// 选择分割位置（在区域中间选择一条线）
	var wx, wy int
	if horizontal {
		// 水平分割：分割线在 y 到 y+height-1 之间
		wy = y + r.Intn(height-1) + 1
		wx = x
	} else {
		// 垂直分割：分割线在 x 到 x+width-1 之间
		wx = x + r.Intn(width-1) + 1
		wy = y
	}

	// 选择通道位置（在分割线上选择一个位置不建墙）
	var px, py int
	if horizontal {
		// 水平分割线上的通道
		px = x + r.Intn(width)
		py = wy
	} else {
		// 垂直分割线上的通道
		px = wx
		py = y + r.Intn(height)
	}

	// 在分割线上建墙，除了通道位置
	if horizontal {
		// 水平分割：在分割线上方添加水平墙，分隔上下
		for i := 0; i < width; i++ {
			cx := x + i
			cy := wy
			if cx == px && cy == py {
				continue // 通道位置不建墙
			}
			// 添加水平墙：分隔 cy-1 和 cy
			if cy > y {
				m.AddWall(cx, cy-1, cx, cy)
			}
		}
	} else {
		// 垂直分割：在分割线左侧添加垂直墙，分隔左右
		for i := 0; i < height; i++ {
			cx := wx
			cy := y + i
			if cx == px && cy == py {
				continue // 通道位置不建墙
			}
			// 添加垂直墙：分隔 cx-1 和 cx
			if cx > x {
				m.AddWall(cx-1, cy, cx, cy)
			}
		}
	}

	// 递归分割子区域
	if horizontal {
		// 上半部分：y 到 wy-1
		divide(m, r, x, y, width, wy-y, chooseOrientation(width, wy-y, r))
		// 下半部分：wy 到 y+height-1
		divide(m, r, x, wy, width, y+height-wy, chooseOrientation(width, y+height-wy, r))
	} else {
		// 左半部分：x 到 wx-1
		divide(m, r, x, y, wx-x, height, chooseOrientation(wx-x, height, r))
		// 右半部分：wx 到 x+width-1
		divide(m, r, wx, y, x+width-wx, height, chooseOrientation(x+width-wx, height, r))
	}
}

// GenerateEllers 使用 Eller 算法生成迷宫
// 特点：逐行生成，内存高效，适合大迷宫
func GenerateEllers(width, height int, seed int64) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	// 每行的集合编号
	sets := make([]int, width)
	// 集合计数器
	setCounter := 1

	// 初始化第一行
	for x := 0; x < width; x++ {
		sets[x] = setCounter
		setCounter++
	}

	// 逐行处理
	for y := 0; y < height; y++ {
		// 水平连接：随机合并同一行中相邻的不同集合
		for x := 0; x < width-1; x++ {
			if sets[x] != sets[x+1] {
				// 最后一行必须全部连接
				if y == height-1 || r.Intn(2) == 0 {
					m.RemoveWall(x, y, x+1, y)
					// 合并集合
					oldSet := sets[x+1]
					for i := 0; i < width; i++ {
						if sets[i] == oldSet {
							sets[i] = sets[x]
						}
					}
				}
			}
		}

		// 最后一行不需要垂直连接
		if y == height-1 {
			break
		}

		// 垂直连接：每个集合至少连接一次
		setMembers := make(map[int][]int)
		for x := 0; x < width; x++ {
			setMembers[sets[x]] = append(setMembers[sets[x]], x)
		}

		// 为每个集合创建垂直连接
		nextSets := make([]int, width)
		for i := range nextSets {
			nextSets[i] = 0
		}

		for set, members := range setMembers {
			// 随机选择至少一个成员向下连接
			sort.Ints(members)
			numDown := 1 + r.Intn(len(members))
			perm := r.Perm(len(members))
			for i := 0; i < numDown; i++ {
				x := members[perm[i]]
				m.RemoveWall(x, y, x, y+1)
				nextSets[x] = set
			}
		}

		// 为未连接的单元格分配新集合
		for x := 0; x < width; x++ {
			if nextSets[x] == 0 {
				nextSets[x] = setCounter
				setCounter++
			}
		}

		sets = nextSets
	}

	return m
}

// GenerateBinaryTree 使用二叉树算法生成迷宫
// 特点：最简单的算法，有对角偏差
// bias: 'N'/'E' = 偏向北和东, 'N'/'W' = 偏向北和西, 'S'/'E' = 偏向南和东, 'S'/'W' = 偏向南和西
func GenerateBinaryTree(width, height int, seed int64, bias string) *Maze {
	m := NewMaze(width, height)
	m.Seed = seed
	r := initRandom(seed)

	// 默认偏北和东
	dir1, dir2 := North, East
	if len(bias) >= 2 {
		switch bias[0] {
		case 'N', 'n':
			dir1 = North
		case 'S', 's':
			dir1 = South
		}
		switch bias[1] {
		case 'E', 'e':
			dir2 = East
		case 'W', 'w':
			dir2 = West
		}
	}

	// 方向偏移
	offsets := map[Direction][2]int{
		North: {0, -1},
		South: {0, 1},
		East:  {1, 0},
		West:  {-1, 0},
	}

	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			// 随机选择方向
			choices := make([]Direction, 0)

			// 检查方向1是否可行
			dx1, dy1 := offsets[dir1][0], offsets[dir1][1]
			nx1, ny1 := x+dx1, y+dy1
			if nx1 >= 0 && nx1 < width && ny1 >= 0 && ny1 < height {
				choices = append(choices, dir1)
			}

			// 检查方向2是否可行
			dx2, dy2 := offsets[dir2][0], offsets[dir2][1]
			nx2, ny2 := x+dx2, y+dy2
			if nx2 >= 0 && nx2 < width && ny2 >= 0 && ny2 < height {
				choices = append(choices, dir2)
			}

			// 随机选择一个方向
			if len(choices) > 0 {
				dir := choices[r.Intn(len(choices))]
				var nx, ny int
				if dir == dir1 {
					nx, ny = nx1, ny1
				} else {
					nx, ny = nx2, ny2
				}
				m.RemoveWall(x, y, nx, ny)
			}
		}
	}

	return m
}

// getUnvisitedNeighbors 获取未访问的邻居
func getUnvisitedNeighbors(m *Maze, x, y int, visited map[[2]int]bool) [][2]int {
	var neighbors [][2]int
	directions := [][2]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}

	for _, d := range directions {
		nx, ny := x+d[0], y+d[1]
		if nx >= 0 && nx < m.Width && ny >= 0 && ny < m.Height {
			if !visited[[2]int{nx, ny}] {
				neighbors = append(neighbors, [2]int{nx, ny})
			}
		}
	}
	return neighbors
}

// addWalls 添加单元格的所有墙到列表
func addWalls(m *Maze, x, y int, walls [][4]int) [][4]int {
	directions := [][2]int{{0, -1}, {1, 0}, {0, 1}, {-1, 0}}

	for _, d := range directions {
		nx, ny := x+d[0], y+d[1]
		if nx >= 0 && nx < m.Width && ny >= 0 && ny < m.Height {
			walls = append(walls, [4]int{x, y, nx, ny})
		}
	}
	return walls
}