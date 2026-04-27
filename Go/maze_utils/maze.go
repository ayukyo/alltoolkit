// Package maze_utils - 迷宫生成与求解工具
// 提供多种迷宫生成算法和求解算法，零外部依赖
package maze_utils

import (
	"errors"
	"fmt"
)

// Direction 表示方向
type Direction int

const (
	North Direction = iota
	East
	South
	West
)

// String 返回方向的字符串表示
func (d Direction) String() string {
	return [...]string{"North", "East", "South", "West"}[d]
}

// Opposite 返回相反方向
func (d Direction) Opposite() Direction {
	return (d + 2) % 4
}

// Cell 表示迷宫中的一个单元格
type Cell struct {
	X, Y  int
	Walls [4]bool // North, East, South, West
	// Walls[i] = true 表示该方向有墙
}

// NewCell 创建新单元格（默认四面有墙）
func NewCell(x, y int) *Cell {
	return &Cell{
		X:     x,
		Y:     y,
		Walls: [4]bool{true, true, true, true},
	}
}

// HasWall 检查是否有指定方向的墙
func (c *Cell) HasWall(d Direction) bool {
	return c.Walls[d]
}

// RemoveWall 移除指定方向的墙
func (c *Cell) RemoveWall(d Direction) {
	c.Walls[d] = false
}

// AddWall 添加指定方向的墙
func (c *Cell) AddWall(d Direction) {
	c.Walls[d] = true
}

// Maze 表示一个迷宫
type Maze struct {
	Width, Height int
	Grid          [][]*Cell
	Start, End    [2]int
	Seed          int64
}

// NewMaze 创建新迷宫
func NewMaze(width, height int) *Maze {
	m := &Maze{
		Width:  width,
		Height: height,
		Grid:   make([][]*Cell, height),
		Start:  [2]int{0, 0},
		End:    [2]int{width - 1, height - 1},
	}
	for y := 0; y < height; y++ {
		m.Grid[y] = make([]*Cell, width)
		for x := 0; x < width; x++ {
			m.Grid[y][x] = NewCell(x, y)
		}
	}
	return m
}

// GetCell 获取指定位置的单元格
func (m *Maze) GetCell(x, y int) (*Cell, error) {
	if x < 0 || x >= m.Width || y < 0 || y >= m.Height {
		return nil, errors.New("cell out of bounds")
	}
	return m.Grid[y][x], nil
}

// RemoveWall 移除两个相邻单元格之间的墙
func (m *Maze) RemoveWall(x1, y1, x2, y2 int) error {
	dx := x2 - x1
	dy := y2 - y1

	if abs(dx)+abs(dy) != 1 {
		return errors.New("cells are not adjacent")
	}

	cell1, err := m.GetCell(x1, y1)
	if err != nil {
		return err
	}
	cell2, err := m.GetCell(x2, y2)
	if err != nil {
		return err
	}

	var dir1, dir2 Direction
	if dx == 1 {
		dir1, dir2 = East, West
	} else if dx == -1 {
		dir1, dir2 = West, East
	} else if dy == 1 {
		dir1, dir2 = South, North
	} else {
		dir1, dir2 = North, South
	}

	cell1.RemoveWall(dir1)
	cell2.RemoveWall(dir2)
	return nil
}

// AddWall 添加两个相邻单元格之间的墙
func (m *Maze) AddWall(x1, y1, x2, y2 int) error {
	dx := x2 - x1
	dy := y2 - y1

	if abs(dx)+abs(dy) != 1 {
		return errors.New("cells are not adjacent")
	}

	cell1, err := m.GetCell(x1, y1)
	if err != nil {
		return err
	}
	cell2, err := m.GetCell(x2, y2)
	if err != nil {
		return err
	}

	var dir1, dir2 Direction
	if dx == 1 {
		dir1, dir2 = East, West
	} else if dx == -1 {
		dir1, dir2 = West, East
	} else if dy == 1 {
		dir1, dir2 = South, North
	} else {
		dir1, dir2 = North, South
	}

	cell1.AddWall(dir1)
	cell2.AddWall(dir2)
	return nil
}

// GetPassages 获取单元格的可通行邻居
func (m *Maze) GetPassages(x, y int) [][2]int {
	cell, err := m.GetCell(x, y)
	if err != nil {
		return nil
	}

	var passages [][2]int
	directions := []struct {
		dir Direction
		dx, dy int
	}{
		{North, 0, -1},
		{East, 1, 0},
		{South, 0, 1},
		{West, -1, 0},
	}

	for _, d := range directions {
		if !cell.HasWall(d.dir) {
			nx, ny := x+d.dx, y+d.dy
			if nx >= 0 && nx < m.Width && ny >= 0 && ny < m.Height {
				passages = append(passages, [2]int{nx, ny})
			}
		}
	}
	return passages
}

// IsPerfect 检查是否为完美迷宫（任意两点间有且只有一条路径）
func (m *Maze) IsPerfect() bool {
	visited := make(map[[2]int]bool)
	var dfs func(x, y, px, py int) bool
	
	dfs = func(x, y, px, py int) bool {
		key := [2]int{x, y}
		if visited[key] {
			return false
		}
		visited[key] = true

		for _, neighbor := range m.GetPassages(x, y) {
			if neighbor[0] == px && neighbor[1] == py {
				continue
			}
			if !dfs(neighbor[0], neighbor[1], x, y) {
				return false
			}
		}
		return true
	}

	if !dfs(0, 0, -1, -1) {
		return false
	}

	// 检查所有单元格都被访问
	return len(visited) == m.Width*m.Height
}

// Copy 创建迷宫的深拷贝
func (m *Maze) Copy() *Maze {
	newMaze := NewMaze(m.Width, m.Height)
	newMaze.Start = m.Start
	newMaze.End = m.End
	newMaze.Seed = m.Seed

	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			newMaze.Grid[y][x].Walls = m.Grid[y][x].Walls
		}
	}
	return newMaze
}

// Path 表示迷宫中的路径
type Path [][2]int

// Contains 检查路径是否包含指定位置
func (p Path) Contains(x, y int) bool {
	for _, pos := range p {
		if pos[0] == x && pos[1] == y {
			return true
		}
	}
	return false
}

// String 返回路径的字符串表示
func (p Path) String() string {
	if len(p) == 0 {
		return "[]"
	}
	s := "["
	for i, pos := range p {
		if i > 0 {
			s += " -> "
		}
		s += fmt.Sprintf("(%d,%d)", pos[0], pos[1])
	}
	return s + "]"
}

// abs 返回整数的绝对值
func abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}