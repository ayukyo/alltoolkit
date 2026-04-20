"""
Maze Serializers - 迷宫序列化工具
==================================

提供迷宫的序列化和反序列化功能：
- JSON格式
- 字典格式
- 文件读写
"""

import json
from typing import Dict, Any, List, Optional
from .maze import Maze, Cell, Direction


def to_dict(maze: Maze) -> Dict[str, Any]:
    """
    将迷宫转换为字典格式
    
    Args:
        maze: 迷宫对象
        
    Returns:
        字典表示
    """
    cells = []
    for y in range(maze.height):
        row = []
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            row.append({
                'walls': [d.name for d in cell.walls],
                'visited': cell.visited,
            })
        cells.append(row)
    
    return {
        'version': '1.0',
        'width': maze.width,
        'height': maze.height,
        'start': list(maze._start) if maze._start else [0, 0],
        'end': list(maze._end) if maze._end else [maze.width - 1, maze.height - 1],
        'cells': cells,
    }


def from_dict(data: Dict[str, Any]) -> Maze:
    """
    从字典创建迷宫
    
    Args:
        data: 字典数据
        
    Returns:
        迷宫对象
    """
    width = data['width']
    height = data['height']
    
    maze = Maze(width, height)
    
    # 设置起点和终点
    if 'start' in data:
        maze.start = tuple(data['start'])
    if 'end' in data:
        maze.end = tuple(data['end'])
    
    # 设置单元格
    cells_data = data.get('cells', [])
    for y, row_data in enumerate(cells_data):
        for x, cell_data in enumerate(row_data):
            cell = maze.get_cell(x, y)
            cell.walls = {Direction[d] for d in cell_data.get('walls', [])}
            cell.visited = cell_data.get('visited', False)
    
    return maze


def to_json(maze: Maze, indent: Optional[int] = 2) -> str:
    """
    将迷宫序列化为JSON字符串
    
    Args:
        maze: 迷宫对象
        indent: 缩进级别
        
    Returns:
        JSON字符串
    """
    return json.dumps(to_dict(maze), indent=indent, ensure_ascii=False)


def from_json(json_str: str) -> Maze:
    """
    从JSON字符串创建迷宫
    
    Args:
        json_str: JSON字符串
        
    Returns:
        迷宫对象
    """
    data = json.loads(json_str)
    return from_dict(data)


def save_to_file(maze: Maze, filepath: str) -> None:
    """
    将迷宫保存到文件
    
    Args:
        maze: 迷宫对象
        filepath: 文件路径
    """
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(to_json(maze))


def load_from_file(filepath: str) -> Maze:
    """
    从文件加载迷宫
    
    Args:
        filepath: 文件路径
        
    Returns:
        迷宫对象
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return from_json(f.read())


def to_binary(maze: Maze) -> bytes:
    """
    将迷宫转换为紧凑的二进制格式
    
    格式：
    - 2字节: 宽度 (uint16, big-endian)
    - 2字节: 高度 (uint16, big-endian)
    - 1字节: 起点X
    - 1字节: 起点Y
    - 1字节: 终点X
    - 1字节: 终点Y
    - N字节: 墙壁位图 (每个单元格4位，表示4个方向)
    
    Args:
        maze: 迷宫对象
        
    Returns:
        二进制数据
    """
    data = bytearray()
    
    # 尺寸
    data.extend(maze.width.to_bytes(2, 'big'))
    data.extend(maze.height.to_bytes(2, 'big'))
    
    # 起点和终点
    data.append(maze.start[0])
    data.append(maze.start[1])
    data.append(maze.end[0])
    data.append(maze.end[1])
    
    # 墙壁位图
    for y in range(maze.height):
        for x in range(0, maze.width, 2):
            cell1 = maze.get_cell(x, y)
            # 每个单元格用4位表示4个墙
            walls1 = 0
            if Direction.NORTH in cell1.walls:
                walls1 |= 0x08
            if Direction.SOUTH in cell1.walls:
                walls1 |= 0x04
            if Direction.EAST in cell1.walls:
                walls1 |= 0x02
            if Direction.WEST in cell1.walls:
                walls1 |= 0x01
            
            if x + 1 < maze.width:
                cell2 = maze.get_cell(x + 1, y)
                walls2 = 0
                if Direction.NORTH in cell2.walls:
                    walls2 |= 0x08
                if Direction.SOUTH in cell2.walls:
                    walls2 |= 0x04
                if Direction.EAST in cell2.walls:
                    walls2 |= 0x02
                if Direction.WEST in cell2.walls:
                    walls2 |= 0x01
                data.append((walls1 << 4) | walls2)
            else:
                data.append(walls1 << 4)
    
    return bytes(data)


def from_binary(data: bytes) -> Maze:
    """
    从二进制数据创建迷宫
    
    Args:
        data: 二进制数据
        
    Returns:
        迷宫对象
    """
    if len(data) < 8:
        raise ValueError("Invalid binary maze data: too short")
    
    # 读取尺寸
    width = int.from_bytes(data[0:2], 'big')
    height = int.from_bytes(data[2:4], 'big')
    
    maze = Maze(width, height)
    
    # 读取起点和终点
    maze.start = (data[4], data[5])
    maze.end = (data[6], data[7])
    
    # 读取墙壁位图
    offset = 8
    for y in range(height):
        for x in range(0, width, 2):
            byte = data[offset]
            offset += 1
            
            # 第一个单元格
            cell1 = maze.get_cell(x, y)
            walls1 = (byte >> 4) & 0x0F
            cell1.walls = set()
            if walls1 & 0x08:
                cell1.walls.add(Direction.NORTH)
            if walls1 & 0x04:
                cell1.walls.add(Direction.SOUTH)
            if walls1 & 0x02:
                cell1.walls.add(Direction.EAST)
            if walls1 & 0x01:
                cell1.walls.add(Direction.WEST)
            
            # 第二个单元格
            if x + 1 < width:
                cell2 = maze.get_cell(x + 1, y)
                walls2 = byte & 0x0F
                cell2.walls = set()
                if walls2 & 0x08:
                    cell2.walls.add(Direction.NORTH)
                if walls2 & 0x04:
                    cell2.walls.add(Direction.SOUTH)
                if walls2 & 0x02:
                    cell2.walls.add(Direction.EAST)
                if walls2 & 0x01:
                    cell2.walls.add(Direction.WEST)
    
    return maze


def to_csv(maze: Maze) -> str:
    """
    将迷宫导出为CSV格式（用于数据分析）
    
    格式：每行一个单元格，包含坐标和墙壁信息
    
    Args:
        maze: 迷宫对象
        
    Returns:
        CSV字符串
    """
    lines = ['x,y,north_wall,south_wall,east_wall,west_wall']
    
    for y in range(maze.height):
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            lines.append(','.join([
                str(x),
                str(y),
                '1' if Direction.NORTH in cell.walls else '0',
                '1' if Direction.SOUTH in cell.walls else '0',
                '1' if Direction.EAST in cell.walls else '0',
                '1' if Direction.WEST in cell.walls else '0',
            ]))
    
    return '\n'.join(lines)