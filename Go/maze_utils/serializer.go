package maze_utils

import (
	"encoding/json"
	"fmt"
	"os"
	"strconv"
	"strings"
)

// MazeJSON JSON 序列化格式
type MazeJSON struct {
	Width  int            `json:"width"`
	Height int            `json:"height"`
	Grid   [][]CellJSON   `json:"grid"`
	Start  [2]int         `json:"start"`
	End    [2]int         `json:"end"`
	Seed   int64          `json:"seed"`
}

// CellJSON 单元格的 JSON 格式
type CellJSON struct {
	X     int  `json:"x"`
	Y     int  `json:"y"`
	Walls [4]bool `json:"walls"` // N, E, S, W
}

// ToJSON 将迷宫序列化为 JSON 字符串
func ToJSON(m *Maze) (string, error) {
	data := MazeJSON{
		Width:  m.Width,
		Height: m.Height,
		Start:  m.Start,
		End:    m.End,
		Seed:   m.Seed,
		Grid:   make([][]CellJSON, m.Height),
	}

	for y := 0; y < m.Height; y++ {
		data.Grid[y] = make([]CellJSON, m.Width)
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]
			data.Grid[y][x] = CellJSON{
				X:     cell.X,
				Y:     cell.Y,
				Walls: cell.Walls,
			}
		}
	}

	bytes, err := json.MarshalIndent(data, "", "  ")
	if err != nil {
		return "", err
	}
	return string(bytes), nil
}

// FromJSON 从 JSON 字符串反序列化迷宫
func FromJSON(jsonStr string) (*Maze, error) {
	var data MazeJSON
	err := json.Unmarshal([]byte(jsonStr), &data)
	if err != nil {
		return nil, err
	}

	m := NewMaze(data.Width, data.Height)
	m.Start = data.Start
	m.End = data.End
	m.Seed = data.Seed

	for y := 0; y < data.Height; y++ {
		for x := 0; x < data.Width; x++ {
			m.Grid[y][x].Walls = data.Grid[y][x].Walls
		}
	}

	return m, nil
}

// ToMap 将迷宫转换为 map 格式
func ToMap(m *Maze) map[string]interface{} {
	grid := make([][]map[string]interface{}, m.Height)
	for y := 0; y < m.Height; y++ {
		grid[y] = make([]map[string]interface{}, m.Width)
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]
			grid[y][x] = map[string]interface{}{
				"x":     cell.X,
				"y":     cell.Y,
				"walls": []bool{cell.Walls[0], cell.Walls[1], cell.Walls[2], cell.Walls[3]},
			}
		}
	}

	return map[string]interface{}{
		"width":  m.Width,
		"height": m.Height,
		"grid":   grid,
		"start":  []int{m.Start[0], m.Start[1]},
		"end":    []int{m.End[0], m.End[1]},
		"seed":   m.Seed,
	}
}

// FromMap 从 map 格式创建迷宫
func FromMap(data map[string]interface{}) (*Maze, error) {
	width := int(data["width"].(float64))
	height := int(data["height"].(float64))

	m := NewMaze(width, height)

	if start, ok := data["start"].([]interface{}); ok {
		m.Start = [2]int{int(start[0].(float64)), int(start[1].(float64))}
	}
	if end, ok := data["end"].([]interface{}); ok {
		m.End = [2]int{int(end[0].(float64)), int(end[1].(float64))}
	}
	if seed, ok := data["seed"].(float64); ok {
		m.Seed = int64(seed)
	}

	gridData, ok := data["grid"].([]interface{})
	if !ok {
		return nil, fmt.Errorf("invalid grid data")
	}

	for y, row := range gridData {
		rowData, ok := row.([]interface{})
		if !ok {
			return nil, fmt.Errorf("invalid row data at y=%d", y)
		}
		for x, cellData := range rowData {
			cell, ok := cellData.(map[string]interface{})
			if !ok {
				return nil, fmt.Errorf("invalid cell data at (%d,%d)", x, y)
			}
			wallsData, ok := cell["walls"].([]interface{})
			if ok {
				for i, w := range wallsData {
					if i < 4 {
						m.Grid[y][x].Walls[i] = w.(bool)
					}
				}
			}
		}
	}

	return m, nil
}

// ToBinary 将迷宫序列化为二进制格式
// 格式: [width:2][height:2][start_x:2][start_y:2][end_x:2][end_y:2][seed:8]
//       [walls: 每个单元格1字节(NESW低4位)]
func ToBinary(m *Maze) []byte {
	// 计算大小: 2 + 2 + 2 + 2 + 2 + 2 + 8 + (width * height) = 20 + (width * height)
	size := 20 + m.Width*m.Height
	data := make([]byte, size)
	pos := 0

	// 写入宽高
	data[pos] = byte(m.Width >> 8)
	data[pos+1] = byte(m.Width)
	pos += 2
	data[pos] = byte(m.Height >> 8)
	data[pos+1] = byte(m.Height)
	pos += 2

	// 写入起点终点
	data[pos] = byte(m.Start[0] >> 8)
	data[pos+1] = byte(m.Start[0])
	pos += 2
	data[pos] = byte(m.Start[1] >> 8)
	data[pos+1] = byte(m.Start[1])
	pos += 2
	data[pos] = byte(m.End[0] >> 8)
	data[pos+1] = byte(m.End[0])
	pos += 2
	data[pos] = byte(m.End[1] >> 8)
	data[pos+1] = byte(m.End[1])
	pos += 2

	// 写入种子
	for i := 7; i >= 0; i-- {
		data[pos+i] = byte(m.Seed >> (8 * (7 - i)))
	}
	pos += 8

	// 写入墙壁数据
	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]
			var b byte
			if cell.Walls[North] {
				b |= 1 << 3
			}
			if cell.Walls[East] {
				b |= 1 << 2
			}
			if cell.Walls[South] {
				b |= 1 << 1
			}
			if cell.Walls[West] {
				b |= 1 << 0
			}
			data[pos] = b
			pos++
		}
	}

	return data
}

// FromBinary 从二进制格式反序列化迷宫
func FromBinary(data []byte) (*Maze, error) {
	if len(data) < 18 {
		return nil, fmt.Errorf("invalid binary data: too short")
	}

	pos := 0

	// 读取宽高
	width := int(data[pos])<<8 | int(data[pos+1])
	pos += 2
	height := int(data[pos])<<8 | int(data[pos+1])
	pos += 2

	if width <= 0 || height <= 0 || width > 10000 || height > 10000 {
		return nil, fmt.Errorf("invalid maze dimensions: %dx%d", width, height)
	}

	// 读取起点终点
	startX := int(data[pos])<<8 | int(data[pos+1])
	pos += 2
	startY := int(data[pos])<<8 | int(data[pos+1])
	pos += 2
	endX := int(data[pos])<<8 | int(data[pos+1])
	pos += 2
	endY := int(data[pos])<<8 | int(data[pos+1])
	pos += 2

	// 读取种子
	var seed int64
	for i := 0; i < 8; i++ {
		seed = seed<<8 | int64(data[pos])
		pos++
	}

	// 验证数据长度
	expectedLen := 20 + width*height
	if len(data) < expectedLen {
		return nil, fmt.Errorf("invalid binary data: expected %d bytes, got %d", expectedLen, len(data))
	}

	// 创建迷宫
	m := NewMaze(width, height)
	m.Start = [2]int{startX, startY}
	m.End = [2]int{endX, endY}
	m.Seed = seed

	// 读取墙壁数据
	for y := 0; y < height; y++ {
		for x := 0; x < width; x++ {
			b := data[pos]
			pos++
			m.Grid[y][x].Walls[North] = (b & (1 << 3)) != 0
			m.Grid[y][x].Walls[East] = (b & (1 << 2)) != 0
			m.Grid[y][x].Walls[South] = (b & (1 << 1)) != 0
			m.Grid[y][x].Walls[West] = (b & (1 << 0)) != 0
		}
	}

	return m, nil
}

// ToCSV 将迷宫导出为 CSV 格式
// 每行: x,y,north,east,south,west
func ToCSV(m *Maze) string {
	var sb strings.Builder
	sb.WriteString("x,y,north,east,south,west\n")

	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			cell := m.Grid[y][x]
			sb.WriteString(fmt.Sprintf("%d,%d,%t,%t,%t,%t\n",
				x, y,
				cell.Walls[North],
				cell.Walls[East],
				cell.Walls[South],
				cell.Walls[West],
			))
		}
	}

	return sb.String()
}

// FromCSV 从 CSV 格式导入迷宫
func FromCSV(csv string) (*Maze, error) {
	lines := strings.Split(csv, "\n")
	if len(lines) < 2 {
		return nil, fmt.Errorf("invalid CSV: no data")
	}

	// 解析所有单元格
	cellMap := make(map[[2]int][4]bool)
	var maxX, maxY int

	for i, line := range lines[1:] {
		line = strings.TrimSpace(line)
		if line == "" {
			continue
		}
		parts := strings.Split(line, ",")
		if len(parts) != 6 {
			return nil, fmt.Errorf("invalid CSV line %d: expected 6 fields", i+2)
		}

		x, _ := strconv.Atoi(parts[0])
		y, _ := strconv.Atoi(parts[1])

		if x > maxX {
			maxX = x
		}
		if y > maxY {
			maxY = y
		}

		walls := [4]bool{}
		walls[North] = parts[2] == "true"
		walls[East] = parts[3] == "true"
		walls[South] = parts[4] == "true"
		walls[West] = parts[5] == "true"

		cellMap[[2]int{x, y}] = walls
	}

	// 创建迷宫
	m := NewMaze(maxX+1, maxY+1)
	for pos, walls := range cellMap {
		if pos[0] >= 0 && pos[0] < m.Width && pos[1] >= 0 && pos[1] < m.Height {
			m.Grid[pos[1]][pos[0]].Walls = walls
		}
	}

	return m, nil
}

// SaveToFile 将迷宫保存到文件
func SaveToFile(m *Maze, filename string) error {
	data, err := ToJSON(m)
	if err != nil {
		return err
	}
	return os.WriteFile(filename, []byte(data), 0644)
}

// LoadFromFile 从文件加载迷宫
func LoadFromFile(filename string) (*Maze, error) {
	data, err := os.ReadFile(filename)
	if err != nil {
		return nil, err
	}
	return FromJSON(string(data))
}

// PathToJSON 将路径序列化为 JSON
func PathToJSON(path Path) string {
	data := make([][2]int, len(path))
	copy(data, path)
	bytes, _ := json.Marshal(data)
	return string(bytes)
}

// PathFromJSON 从 JSON 反序列化路径
func PathFromJSON(jsonStr string) (Path, error) {
	var path Path
	err := json.Unmarshal([]byte(jsonStr), &path)
	return path, err
}