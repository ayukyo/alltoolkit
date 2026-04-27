package maze_utils

import (
	"fmt"
	"strings"
)

// RenderStyle 渲染样式
type RenderStyle string

const (
	StyleBox    RenderStyle = "box"    // 标准 Unicode 方框
	StyleRound  RenderStyle = "round"  // 圆角样式
	StyleDouble RenderStyle = "double" // 双线样式
	StyleASCII  RenderStyle = "ascii"  // 纯 ASCII
	StyleBlock  RenderStyle = "block"  // 方块样式
)

// 墙壁字符定义
var wallChars = map[RenderStyle]struct {
	corner, horizontal, vertical string
	topLeft, topRight, bottomLeft, bottomRight string
	leftT, rightT, topT, bottomT string
	cross string
}{
	StyleBox: {
		corner:      "+",
		horizontal:  "─",
		vertical:    "│",
		topLeft:     "┌",
		topRight:    "┐",
		bottomLeft:  "└",
		bottomRight: "┘",
		leftT:       "├",
		rightT:      "┤",
		topT:        "┬",
		bottomT:     "┴",
		cross:       "┼",
	},
	StyleRound: {
		corner:      "+",
		horizontal:  "─",
		vertical:    "│",
		topLeft:     "╭",
		topRight:    "╮",
		bottomLeft:  "╰",
		bottomRight: "╯",
		leftT:       "├",
		rightT:      "┤",
		topT:        "┬",
		bottomT:     "┴",
		cross:       "┼",
	},
	StyleDouble: {
		corner:      "+",
		horizontal:  "═",
		vertical:    "║",
		topLeft:     "╔",
		topRight:    "╗",
		bottomLeft:  "╚",
		bottomRight: "╝",
		leftT:       "╠",
		rightT:      "╣",
		topT:        "╦",
		bottomT:     "╩",
		cross:       "╬",
	},
	StyleASCII: {
		corner:      "+",
		horizontal:  "-",
		vertical:    "|",
		topLeft:     "+",
		topRight:    "+",
		bottomLeft:  "+",
		bottomRight: "+",
		leftT:       "+",
		rightT:      "+",
		topT:        "+",
		bottomT:     "+",
		cross:       "+",
	},
	StyleBlock: {
		corner:      "█",
		horizontal:  "█",
		vertical:    "█",
		topLeft:     "█",
		topRight:    "█",
		bottomLeft:  "█",
		bottomRight: "█",
		leftT:       "█",
		rightT:      "█",
		topT:        "█",
		bottomT:     "█",
		cross:       "█",
	},
}

// RenderASCII 使用 ASCII 字符渲染迷宫
func RenderASCII(m *Maze) string {
	return renderUnicode(m, nil, StyleASCII, ' ', 'S', 'E', '#')
}

// RenderUnicode 使用 Unicode 字符渲染迷宫
func RenderUnicode(m *Maze, style RenderStyle) string {
	return renderUnicode(m, nil, style, ' ', 'S', 'E', 0)
}

// RenderPath 渲染带有路径的迷宫
func RenderPath(m *Maze, path Path, style RenderStyle) string {
	pathSet := make(map[[2]int]int)
	for i, pos := range path {
		pathSet[pos] = i
	}
	return renderUnicode(m, pathSet, style, '·', 'S', 'E', 0)
}

// RenderPathDetailed 渲染带有路径方向的迷宫
func RenderPathDetailed(m *Maze, path Path, style RenderStyle) string {
	if len(path) == 0 {
		return RenderUnicode(m, style)
	}

	// 计算每个位置的方向
	pathDir := make(map[[2]int]rune)
	for i, pos := range path {
		if i == 0 {
			if len(path) > 1 {
				next := path[1]
				pathDir[pos] = getDirectionChar(pos, next)
			}
		} else if i == len(path)-1 {
			pathDir[pos] = '●'
		} else {
			next := path[i+1]
			pathDir[pos] = getDirectionChar(pos, next)
		}
	}

	return renderWithDirection(m, pathDir, style)
}

// getDirectionChar 获取方向字符
func getDirectionChar(from, to [2]int) rune {
	dx := to[0] - from[0]
	dy := to[1] - from[1]

	switch {
	case dx == 1:
		return '→'
	case dx == -1:
		return '←'
	case dy == 1:
		return '↓'
	case dy == -1:
		return '↑'
	default:
		return '·'
	}
}

// renderUnicode 渲染迷宫的核心函数
func renderUnicode(m *Maze, pathSet map[[2]int]int, style RenderStyle, emptyChar, startChar, endChar rune, pathChar rune) string {
	chars, ok := wallChars[style]
	if !ok {
		chars = wallChars[StyleBox]
	}

	var sb strings.Builder

	// 渲染顶部边界
	sb.WriteString(chars.topLeft)
	for x := 0; x < m.Width; x++ {
		sb.WriteString(chars.horizontal)
		sb.WriteString(chars.horizontal)
		if x < m.Width-1 {
			sb.WriteString(chars.topT)
		}
	}
	sb.WriteString(chars.topRight)
	sb.WriteString("\n")

	// 渲染每行
	for y := 0; y < m.Height; y++ {
		// 渲染单元格内容
		sb.WriteString(chars.vertical)
		for x := 0; x < m.Width; x++ {
			pos := [2]int{x, y}
			cell := m.Grid[y][x]

			// 渲染单元格内容
			var content rune
			if pos == m.Start {
				content = startChar
			} else if pos == m.End {
				content = endChar
			} else if _, inPath := pathSet[pos]; inPath {
				if pathChar != 0 {
					content = pathChar
				} else {
					content = '·'
				}
			} else {
				content = emptyChar
			}
			sb.WriteRune(content)
			sb.WriteRune(' ')

			// 渲染右侧墙
			if x < m.Width-1 {
				if cell.HasWall(East) {
					sb.WriteString(chars.vertical)
				} else {
					sb.WriteRune(' ')
				}
			}
		}
		sb.WriteString(chars.vertical)
		sb.WriteString("\n")

		// 渲染底部边界
		if y < m.Height-1 {
			sb.WriteString(chars.leftT)
			for x := 0; x < m.Width; x++ {
				cell := m.Grid[y][x]
				if cell.HasWall(South) {
					sb.WriteString(chars.horizontal)
				} else {
					sb.WriteRune(' ')
				}
				sb.WriteString(chars.horizontal)
				if x < m.Width-1 {
					// 检查交叉点
					sb.WriteString(chars.cross)
				}
			}
			sb.WriteString(chars.rightT)
			sb.WriteString("\n")
		}
	}

	// 渲染底部边界
	sb.WriteString(chars.bottomLeft)
	for x := 0; x < m.Width; x++ {
		sb.WriteString(chars.horizontal)
		sb.WriteString(chars.horizontal)
		if x < m.Width-1 {
			sb.WriteString(chars.bottomT)
		}
	}
	sb.WriteString(chars.bottomRight)
	sb.WriteString("\n")

	return sb.String()
}

// renderWithDirection 渲染带有方向的迷宫
func renderWithDirection(m *Maze, pathDir map[[2]int]rune, style RenderStyle) string {
	chars, ok := wallChars[style]
	if !ok {
		chars = wallChars[StyleBox]
	}

	var sb strings.Builder

	// 渲染顶部边界
	sb.WriteString(chars.topLeft)
	for x := 0; x < m.Width; x++ {
		sb.WriteString(chars.horizontal)
		sb.WriteString(chars.horizontal)
		if x < m.Width-1 {
			sb.WriteString(chars.topT)
		}
	}
	sb.WriteString(chars.topRight)
	sb.WriteString("\n")

	// 渲染每行
	for y := 0; y < m.Height; y++ {
		// 渲染单元格内容
		sb.WriteString(chars.vertical)
		for x := 0; x < m.Width; x++ {
			pos := [2]int{x, y}

			// 渲染单元格内容
			var content rune
			if pos == m.Start {
				content = 'S'
			} else if pos == m.End {
				content = 'E'
			} else if dir, ok := pathDir[pos]; ok {
				content = dir
			} else {
				content = ' '
			}
			sb.WriteRune(content)
			sb.WriteRune(' ')

			// 渲染右侧墙
			cell := m.Grid[y][x]
			if x < m.Width-1 {
				if cell.HasWall(East) {
					sb.WriteString(chars.vertical)
				} else {
					sb.WriteRune(' ')
				}
			}
		}
		sb.WriteString(chars.vertical)
		sb.WriteString("\n")

		// 渲染底部边界
		if y < m.Height-1 {
			sb.WriteString(chars.leftT)
			for x := 0; x < m.Width; x++ {
				cell := m.Grid[y][x]
				if cell.HasWall(South) {
					sb.WriteString(chars.horizontal)
				} else {
					sb.WriteRune(' ')
				}
				sb.WriteString(chars.horizontal)
				if x < m.Width-1 {
					sb.WriteString(chars.cross)
				}
			}
			sb.WriteString(chars.rightT)
			sb.WriteString("\n")
		}
	}

	// 渲染底部边界
	sb.WriteString(chars.bottomLeft)
	for x := 0; x < m.Width; x++ {
		sb.WriteString(chars.horizontal)
		sb.WriteString(chars.horizontal)
		if x < m.Width-1 {
			sb.WriteString(chars.bottomT)
		}
	}
	sb.WriteString(chars.bottomRight)
	sb.WriteString("\n")

	return sb.String()
}

// RenderSimple 使用简单 ASCII 渲染迷宫（紧凑格式）
func RenderSimple(m *Maze) string {
	var sb strings.Builder

	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]

			// 上墙
			if y == 0 {
				if x == 0 {
					sb.WriteString("+")
				}
				if cell.HasWall(North) {
					sb.WriteString("--")
				} else {
					sb.WriteString("  ")
				}
				sb.WriteString("+")
			}
		}
		if y == 0 {
			sb.WriteString("\n")
		}

		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]

			// 左墙
			if x == 0 {
				if cell.HasWall(West) {
					sb.WriteString("|")
				} else {
					sb.WriteString(" ")
				}
			}

			// 单元格内容
			pos := [2]int{x, y}
			if pos == m.Start {
				sb.WriteString("S ")
			} else if pos == m.End {
				sb.WriteString("E ")
			} else {
				sb.WriteString("  ")
			}

			// 右墙
			if cell.HasWall(East) {
				sb.WriteString("|")
			} else {
				sb.WriteString(" ")
			}
		}
		sb.WriteString("\n")

		// 底墙
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]

			if x == 0 {
				sb.WriteString("+")
			}
			if cell.HasWall(South) {
				sb.WriteString("--")
			} else {
				sb.WriteString("  ")
			}
			sb.WriteString("+")
		}
		sb.WriteString("\n")
	}

	return sb.String()
}

// RenderAsGrid 将迷宫渲染为简单的网格字符（用于调试）
func RenderAsGrid(m *Maze) string {
	var sb strings.Builder

	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]
			sb.WriteString("[")
			if cell.HasWall(North) {
				sb.WriteString("N")
			}
			if cell.HasWall(East) {
				sb.WriteString("E")
			}
			if cell.HasWall(South) {
				sb.WriteString("S")
			}
			if cell.HasWall(West) {
				sb.WriteString("W")
			}
			sb.WriteString("] ")
		}
		sb.WriteString("\n")
	}

	return sb.String()
}

// PrintMaze 打印迷宫到控制台
func PrintMaze(m *Maze) {
	fmt.Print(RenderUnicode(m, StyleBox))
}

// PrintPath 打印带路径的迷宫到控制台
func PrintPath(m *Maze, path Path) {
	fmt.Print(RenderPath(m, path, StyleBox))
}