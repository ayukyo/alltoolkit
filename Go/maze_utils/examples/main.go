package main

import (
	"fmt"
	"time"

	maze "github.com/ayukyo/alltoolkit/Go/maze_utils"
)

func main() {
	fmt.Println("=== Maze Utils 示例 ===")
	fmt.Println()

	// 示例1: 使用 DFS 生成迷宫
	fmt.Println("【示例1】DFS 生成迷宫")
	m := maze.GenerateDFS(10, 10, 42)
	fmt.Println(maze.RenderUnicode(m, maze.StyleBox))
	fmt.Println()

	// 示例2: 使用 BFS 求解迷宫
	fmt.Println("【示例2】BFS 求解迷宫")
	path := maze.SolveBFS(m, m.Start, m.End)
	if path != nil {
		fmt.Printf("路径长度: %d 步\n", len(path))
		fmt.Println("路径:", path.String())
		fmt.Println()
		fmt.Println(maze.RenderPath(m, path, maze.StyleBox))
	} else {
		fmt.Println("无法找到路径")
	}
	fmt.Println()

	// 示例3: 不同生成算法
	fmt.Println("【示例3】不同生成算法对比")
	fmt.Println("Prim 算法:")
	mPrim := maze.GeneratePrim(8, 8, 42)
	fmt.Println(maze.RenderASCII(mPrim))
	fmt.Println()

	fmt.Println("Kruskal 算法:")
	mKruskal := maze.GenerateKruskal(8, 8, 42)
	fmt.Println(maze.RenderASCII(mKruskal))
	fmt.Println()

	fmt.Println("Eller 算法:")
	mEller := maze.GenerateEllers(8, 8, 42)
	fmt.Println(maze.RenderASCII(mEller))
	fmt.Println()

	// 示例4: 不同渲染样式
	fmt.Println("【示例4】不同渲染样式")
	mSmall := maze.GenerateDFS(5, 5, 42)

	fmt.Println("标准样式 (Box):")
	fmt.Println(maze.RenderUnicode(mSmall, maze.StyleBox))

	fmt.Println("圆角样式 (Round):")
	fmt.Println(maze.RenderUnicode(mSmall, maze.StyleRound))

	fmt.Println("双线样式 (Double):")
	fmt.Println(maze.RenderUnicode(mSmall, maze.StyleDouble))

	fmt.Println("方块样式 (Block):")
	fmt.Println(maze.RenderUnicode(mSmall, maze.StyleBlock))
	fmt.Println()

	// 示例5: A* 算法求解
	fmt.Println("【示例5】A* 算法求解大迷宫")
	mLarge := maze.GenerateKruskal(20, 20, 42)
	start := time.Now()
	astarPath := maze.SolveAStar(mLarge, mLarge.Start, mLarge.End)
	elapsed := time.Since(start)
	fmt.Printf("A* 求解 20x20 迷宫: %d 步, 耗时 %v\n", len(astarPath), elapsed)

	start = time.Now()
	bfsPath := maze.SolveBFS(mLarge, mLarge.Start, mLarge.End)
	elapsed = time.Since(start)
	fmt.Printf("BFS 求解 20x20 迷宫: %d 步, 耗时 %v\n", len(bfsPath), elapsed)

	// 验证路径长度相同（完美迷宫）
	if len(astarPath) == len(bfsPath) {
		fmt.Println("✓ A* 和 BFS 找到了相同长度的路径（最短路径）")
	}
	fmt.Println()

	// 示例6: 序列化与反序列化
	fmt.Println("【示例6】序列化与反序列化")
	jsonStr, err := maze.ToJSON(mSmall)
	if err != nil {
		fmt.Println("JSON 序列化失败:", err)
	} else {
		fmt.Println("JSON 格式:")
		fmt.Println(jsonStr[:200] + "...")
		fmt.Println()

		mRestored, err := maze.FromJSON(jsonStr)
		if err != nil {
			fmt.Println("JSON 反序列化失败:", err)
		} else {
			fmt.Println("反序列化后的迷宫:")
			fmt.Println(maze.RenderASCII(mRestored))
		}
	}
	fmt.Println()

	// 示例7: 二进制格式
	fmt.Println("【示例7】二进制格式")
	binaryData := maze.ToBinary(mSmall)
	fmt.Printf("二进制大小: %d 字节 (JSON大小约 %d 字节)\n", len(binaryData), len(jsonStr))
	fmt.Println()

	// 示例8: 自定义起点终点
	fmt.Println("【示例8】自定义起点终点")
	mCustom := maze.GenerateDFS(10, 10, 42)
	mCustom.Start = [2]int{0, 5}
	mCustom.End = [2]int{9, 5}
	customPath := maze.SolveBFS(mCustom, mCustom.Start, mCustom.End)
	fmt.Printf("从 (0,5) 到 (9,5) 的路径长度: %d\n", len(customPath))
	fmt.Println()

	// 示例9: 递归分割算法
	fmt.Println("【示例9】递归分割算法")
	mDivision := maze.GenerateRecursiveDivision(15, 15, 42)
	pathDivision := maze.SolveBFS(mDivision, mDivision.Start, mDivision.End)
	fmt.Printf("递归分割迷宫路径长度: %d\n", len(pathDivision))
	fmt.Println(maze.RenderASCII(mDivision))
	fmt.Println()

	// 示例10: 二叉树算法
	fmt.Println("【示例10】二叉树算法（不同偏差）")
	fmt.Println("偏北和东:")
	mBinaryNE := maze.GenerateBinaryTree(8, 8, 42, "NE")
	fmt.Println(maze.RenderASCII(mBinaryNE))

	fmt.Println("偏南和西:")
	mBinarySW := maze.GenerateBinaryTree(8, 8, 42, "SW")
	fmt.Println(maze.RenderASCII(mBinarySW))
	fmt.Println()

	// 示例11: 墙跟随算法
	fmt.Println("【示例11】墙跟随算法")
	mWall := maze.GenerateDFS(15, 15, 42)
	pathLeft := maze.SolveWallFollower(mWall, mWall.Start, mWall.End, "left")
	pathRight := maze.SolveWallFollower(mWall, mWall.Start, mWall.End, "right")
	fmt.Printf("左手跟随路径长度: %d\n", len(pathLeft))
	fmt.Printf("右手跟随路径长度: %d\n", len(pathRight))
	fmt.Println()

	// 示例12: 检查完美迷宫
	fmt.Println("【示例12】检查完美迷宫")
	fmt.Printf("DFS 迷宫是否完美: %v\n", maze.GenerateDFS(10, 10, 42).IsPerfect())
	fmt.Printf("Prim 迷宫是否完美: %v\n", maze.GeneratePrim(10, 10, 42).IsPerfect())
	fmt.Printf("Kruskal 迷宫是否完美: %v\n", maze.GenerateKruskal(10, 10, 42).IsPerfect())
	fmt.Println()

	// 示例13: 性能测试
	fmt.Println("【示例13】性能测试")
	sizes := []struct{ w, h int }{{10, 10}, {50, 50}, {100, 100}}
	for _, size := range sizes {
		start := time.Now()
		mBig := maze.GenerateEllers(size.w, size.h, 42)
		genTime := time.Since(start)

		start = time.Now()
		path := maze.SolveBFS(mBig, mBig.Start, mBig.End)
		solveTime := time.Since(start)

		fmt.Printf("%dx%d: 生成 %v, 求解 %v, 路径长度 %d\n",
			size.w, size.h, genTime, solveTime, len(path))
	}
	fmt.Println()

	fmt.Println("=== 示例完成 ===")
}