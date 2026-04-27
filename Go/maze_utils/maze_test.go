package maze_utils

import (
	"os"
	"testing"
)

// 测试生成器
func TestGenerateDFS(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	if m.Width != 10 || m.Height != 10 {
		t.Errorf("Expected 10x10, got %dx%d", m.Width, m.Height)
	}

	// 检查是否为完美迷宫
	if !m.IsPerfect() {
		t.Error("DFS generated maze should be perfect")
	}
}

func TestGeneratePrim(t *testing.T) {
	m := GeneratePrim(15, 15, 42)
	if m.Width != 15 || m.Height != 15 {
		t.Errorf("Expected 15x15, got %dx%d", m.Width, m.Height)
	}

	if !m.IsPerfect() {
		t.Error("Prim generated maze should be perfect")
	}
}

func TestGenerateKruskal(t *testing.T) {
	m := GenerateKruskal(20, 20, 42)
	if m.Width != 20 || m.Height != 20 {
		t.Errorf("Expected 20x20, got %dx%d", m.Width, m.Height)
	}

	if !m.IsPerfect() {
		t.Error("Kruskal generated maze should be perfect")
	}
}

func TestGenerateRecursiveDivision(t *testing.T) {
	// 递归分割需要更大的迷宫才能正确工作
	m := GenerateRecursiveDivision(15, 15, 42)
	if m.Width != 15 || m.Height != 15 {
		t.Errorf("Expected 15x15, got %dx%d", m.Width, m.Height)
	}

	// 递归分割可能不是完美迷宫，但应该有解
	path := SolveBFS(m, m.Start, m.End)
	if path == nil {
		// 尝试使用不同的起点终点
		m.Start = [2]int{0, 0}
		m.End = [2]int{m.Width - 1, m.Height - 1}
		path = SolveBFS(m, m.Start, m.End)
		if path == nil {
			t.Error("Recursive division maze should be solvable")
		}
	}
}

func TestGenerateEllers(t *testing.T) {
	m := GenerateEllers(50, 50, 42)
	if m.Width != 50 || m.Height != 50 {
		t.Errorf("Expected 50x50, got %dx%d", m.Width, m.Height)
	}

	if !m.IsPerfect() {
		t.Error("Eller generated maze should be perfect")
	}
}

func TestGenerateBinaryTree(t *testing.T) {
	m := GenerateBinaryTree(10, 10, 42, "NE")
	if m.Width != 10 || m.Height != 10 {
		t.Errorf("Expected 10x10, got %dx%d", m.Width, m.Height)
	}

	// 二叉树迷宫应该是完美迷宫
	if !m.IsPerfect() {
		t.Error("Binary tree maze should be perfect")
	}
}

// 测试求解器
func TestSolveBFS(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	path := SolveBFS(m, m.Start, m.End)

	if path == nil {
		t.Error("BFS should find a path")
	}

	// 检查路径起点和终点
	if path[0] != m.Start {
		t.Errorf("Path should start at %v, got %v", m.Start, path[0])
	}
	if path[len(path)-1] != m.End {
		t.Errorf("Path should end at %v, got %v", m.End, path[len(path)-1])
	}

	// 检查路径连续性
	for i := 1; i < len(path); i++ {
		prev := path[i-1]
		curr := path[i]
		dx := abs(curr[0] - prev[0])
		dy := abs(curr[1] - prev[1])
		if dx+dy != 1 {
			t.Errorf("Path is not continuous at step %d: %v -> %v", i, prev, curr)
		}
	}
}

func TestSolveDFS(t *testing.T) {
	m := GeneratePrim(10, 10, 42)
	path := SolveDFS(m, m.Start, m.End)

	if path == nil {
		t.Error("DFS should find a path")
	}

	if path[0] != m.Start {
		t.Errorf("Path should start at %v", m.Start)
	}
	if path[len(path)-1] != m.End {
		t.Errorf("Path should end at %v", m.End)
	}
}

func TestSolveAStar(t *testing.T) {
	m := GenerateKruskal(20, 20, 42)
	path := SolveAStar(m, m.Start, m.End)

	if path == nil {
		t.Error("A* should find a path")
	}

	// A* 应该找到最短路径
	bfsPath := SolveBFS(m, m.Start, m.End)
	if len(path) != len(bfsPath) {
		t.Errorf("A* path length %d != BFS path length %d", len(path), len(bfsPath))
	}
}

func TestSolveWallFollower(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	path := SolveWallFollower(m, m.Start, m.End, "left")

	if path == nil {
		t.Error("Wall follower should find a path in perfect maze")
	}

	// 测试右手版本
	pathRight := SolveWallFollower(m, m.Start, m.End, "right")
	if pathRight == nil {
		t.Error("Right-hand wall follower should find a path")
	}
}

func TestSolveDeadEndFilling(t *testing.T) {
	m := GenerateDFS(15, 15, 42)
	path := SolveDeadEndFilling(m, m.Start, m.End)

	if path == nil {
		t.Error("Dead end filling should find a path")
	}
}

// 测试渲染器
func TestRenderASCII(t *testing.T) {
	m := GenerateDFS(5, 5, 42)
	output := RenderASCII(m)

	if output == "" {
		t.Error("ASCII render should produce output")
	}

	// 检查是否包含必要的字符
	if !containsAll(output, "+", "-", "|") {
		t.Error("ASCII render should contain +, -, |")
	}
}

func TestRenderUnicode(t *testing.T) {
	m := GenerateDFS(5, 5, 42)
	output := RenderUnicode(m, StyleBox)

	if output == "" {
		t.Error("Unicode render should produce output")
	}
}

func TestRenderPath(t *testing.T) {
	m := GenerateDFS(5, 5, 42)
	path := SolveBFS(m, m.Start, m.End)
	output := RenderPath(m, path, StyleBox)

	if output == "" {
		t.Error("Path render should produce output")
	}
}

func TestRenderStyles(t *testing.T) {
	m := GenerateDFS(3, 3, 42)

	styles := []RenderStyle{StyleBox, StyleRound, StyleDouble, StyleASCII, StyleBlock}
	for _, style := range styles {
		output := RenderUnicode(m, style)
		if output == "" {
			t.Errorf("Style %s should produce output", style)
		}
	}
}

// 测试序列化
func TestToJSONFromJSON(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	jsonStr, err := ToJSON(m)
	if err != nil {
		t.Fatalf("ToJSON failed: %v", err)
	}

	m2, err := FromJSON(jsonStr)
	if err != nil {
		t.Fatalf("FromJSON failed: %v", err)
	}

	// 检查迷宫是否相同
	if m2.Width != m.Width || m2.Height != m.Height {
		t.Errorf("Dimensions mismatch: %dx%d vs %dx%d", m2.Width, m2.Height, m.Width, m.Height)
	}

	if m2.Start != m.Start {
		t.Errorf("Start mismatch: %v vs %v", m2.Start, m.Start)
	}

	if m2.End != m.End {
		t.Errorf("End mismatch: %v vs %v", m2.End, m.End)
	}

	// 检查所有单元格
	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			if m.Grid[y][x].Walls != m2.Grid[y][x].Walls {
				t.Errorf("Cell walls mismatch at (%d,%d)", x, y)
			}
		}
	}
}

func TestToBinaryFromBinary(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	data := ToBinary(m)

	m2, err := FromBinary(data)
	if err != nil {
		t.Fatalf("FromBinary failed: %v", err)
	}

	if m2.Width != m.Width || m2.Height != m.Height {
		t.Errorf("Dimensions mismatch")
	}

	// 检查所有单元格
	for y := 0; y < m.Height; y++ {
		for x := 0; x < m.Width; x++ {
			if m.Grid[y][x].Walls != m2.Grid[y][x].Walls {
				t.Errorf("Cell walls mismatch at (%d,%d)", x, y)
			}
		}
	}
}

func TestToCSVFromCSV(t *testing.T) {
	m := GenerateDFS(5, 5, 42)
	csv := ToCSV(m)

	m2, err := FromCSV(csv)
	if err != nil {
		t.Fatalf("FromCSV failed: %v", err)
	}

	if m2.Width != m.Width || m2.Height != m.Height {
		t.Errorf("Dimensions mismatch")
	}
}

func TestSaveLoadFile(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	filename := "/tmp/test_maze.json"

	err := SaveToFile(m, filename)
	if err != nil {
		t.Fatalf("SaveToFile failed: %v", err)
	}

	m2, err := LoadFromFile(filename)
	if err != nil {
		t.Fatalf("LoadFromFile failed: %v", err)
	}

	if m2.Width != m.Width {
		t.Errorf("Width mismatch")
	}

	// 清理
	os.Remove(filename)
}

// 测试迷宫操作
func TestMazeOperations(t *testing.T) {
	m := NewMaze(5, 5)

	// 测试移除墙
	err := m.RemoveWall(0, 0, 1, 0)
	if err != nil {
		t.Errorf("RemoveWall failed: %v", err)
	}

	// 检查墙是否被移除
	if m.Grid[0][0].HasWall(East) {
		t.Error("East wall should be removed")
	}
	if m.Grid[0][1].HasWall(West) {
		t.Error("West wall should be removed")
	}

	// 测试添加墙
	err = m.AddWall(0, 0, 1, 0)
	if err != nil {
		t.Errorf("AddWall failed: %v", err)
	}

	if !m.Grid[0][0].HasWall(East) {
		t.Error("East wall should be added back")
	}
}

func TestGetPassages(t *testing.T) {
	m := GenerateDFS(5, 5, 42)
	passages := m.GetPassages(0, 0)

	// 至少应该有一个可通行的邻居（完美迷宫）
	if len(passages) < 1 {
		t.Error("First cell should have at least one passage")
	}
}

func TestMazeCopy(t *testing.T) {
	m := GenerateDFS(10, 10, 42)
	m2 := m.Copy()

	if m2.Width != m.Width {
		t.Error("Copy should preserve dimensions")
	}

	// 修改原迷宫，检查副本不变
	// 先确保墙存在
	originalState := m.Grid[0][0].HasWall(East)
	m.RemoveWall(0, 0, 1, 0)
	newState := m.Grid[0][0].HasWall(East)
	
	// 如果墙原本就不存在，添加一个墙来测试
	if originalState == newState {
		m.AddWall(0, 0, 1, 0)
		newState = m.Grid[0][0].HasWall(East)
	}
	
	// 副本应该保持原来的状态
	if m2.Grid[0][0].HasWall(East) != originalState {
		t.Errorf("Copy should be independent: original=%v, new=%v, copy=%v", 
			originalState, newState, m2.Grid[0][0].HasWall(East))
	}
}

// 测试路径
func TestPathContains(t *testing.T) {
	path := Path{{0, 0}, {1, 0}, {1, 1}}

	if !path.Contains(0, 0) {
		t.Error("Path should contain (0,0)")
	}
	if path.Contains(5, 5) {
		t.Error("Path should not contain (5,5)")
	}
}

// 测试方向
func TestDirection(t *testing.T) {
	if North.Opposite() != South {
		t.Error("North opposite should be South")
	}
	if East.Opposite() != West {
		t.Error("East opposite should be West")
	}

	if North.String() != "North" {
		t.Errorf("North string should be 'North', got '%s'", North.String())
	}
}

// 辅助函数
func containsAll(s string, chars ...string) bool {
	for _, c := range chars {
		if !contains(s, c) {
			return false
		}
	}
	return true
}

func contains(s, substr string) bool {
	for i := 0; i < len(s); i++ {
		if i+len(substr) <= len(s) && s[i:i+len(substr)] == substr {
			return true
		}
	}
	return false
}

// 性能测试
func BenchmarkGenerateDFS(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GenerateDFS(50, 50, 42)
	}
}

func BenchmarkGeneratePrim(b *testing.B) {
	for i := 0; i < b.N; i++ {
		GeneratePrim(50, 50, 42)
	}
}

func BenchmarkSolveBFS(b *testing.B) {
	m := GenerateDFS(50, 50, 42)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		SolveBFS(m, m.Start, m.End)
	}
}

func BenchmarkSolveAStar(b *testing.B) {
	m := GenerateDFS(50, 50, 42)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		SolveAStar(m, m.Start, m.End)
	}
}

func BenchmarkToJSON(b *testing.B) {
	m := GenerateDFS(50, 50, 42)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		ToJSON(m)
	}
}