"""Rotation Utils 使用示例"""
import sys
sys.path.insert(0, '..')
from mod import *

def basic_examples():
    print("=" * 50)
    print("基础数组旋转")
    print("=" * 50)
    arr = [1, 2, 3, 4, 5, 6, 7]
    print(f"原数组: {arr}")
    print(f"左旋 3 步: {rotate_left_simple(arr, 3)}")
    print(f"右旋 3 步: {rotate_right_simple(arr, 3)}")
    
    print("\n位旋转 (8位):")
    val = 0b10110011
    print(f"原值: {bin(val)[2:].zfill(8)} = {val}")
    print(f"左旋 3: {bin(rotate_left_bits(val, 3, 8))[2:].zfill(8)} = {rotate_left_bits(val, 3, 8)}")
    print(f"右旋 3: {bin(rotate_right_bits(val, 3, 8))[2:].zfill(8)} = {rotate_right_bits(val, 3, 8)}")
    
    print("\n矩阵旋转:")
    matrix = [[1,2,3],[4,5,6],[7,8,9]]
    print("原矩阵:")
    for r in matrix: print(f"  {r}")
    print("顺时针 90°:")
    for r in rotate_matrix_90_clockwise(matrix): print(f"  {r}")
    
    print("\n字符串旋转:")
    s = "hello"
    print(f"原: '{s}'")
    print(f"左旋 2: '{rotate_string_left(s, 2)}'")
    print(f"'llohe' 是 'hello' 的旋转: {is_rotation('hello', 'llohe')}")

def rotator_examples():
    print("\n" + "=" * 50)
    print("Rotator 类 - 链式调用")
    print("=" * 50)
    r = Rotator([1, 2, 3, 4, 5])
    print(f"初始: {r.result()}")
    print(f"左旋2 + 右旋1: {r.left(2).right(1).result()}")
    
    br = BitRotator(0b10110011, 8)
    print(f"\nBitRotator 初始: {br.binary()}")
    print(f"左旋 3: {br.left(3).binary()}")

if __name__ == "__main__":
    basic_examples()
    rotator_examples()
    print("\n示例运行完成!")
