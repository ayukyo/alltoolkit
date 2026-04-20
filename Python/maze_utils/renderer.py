"""
Maze Renderers - 迷宫可视化渲染器
=================================

提供多种迷宫可视化方式：
- ASCII渲染
- Unicode渲染
- 路径可视化
"""

from typing import Optional, List, Tuple, Set
from .maze import Maze, Direction

# 类型别名
Position = Tuple[int, int]
Path = List[Position]


def render_ascii(maze: Maze, path: Optional[Path] = None,
                 show_start_end: bool = True) -> str:
    """
    将迷宫渲染为ASCII字符
    
    使用标准ASCII字符：
    - '+' 表示角落
    - '-' 表示水平墙
    - '|' 表示垂直墙
    - '#' 表示路径
    - 'S' 表示起点
    - 'E' 表示终点
    
    Args:
        maze: 迷宫对象
        path: 可选的路径列表
        show_start_end: 是否显示起点和终点标记
        
    Returns:
        ASCII字符串表示
    """
    path_set = set(path) if path else set()
    
    # 计算每行字符串的行数
    # 每个单元格占用 2 个字符宽度（包括墙壁）
    # 每个单元格占用 2 个字符高度（包括墙壁）
    lines = []
    
    # 顶部边界
    top_line = '+'
    for x in range(maze.width):
        top_line += '--+'
    lines.append(top_line)
    
    for y in range(maze.height):
        # 单元格行
        cell_line = '|'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            # 单元格内容
            if show_start_end and (x, y) == maze.start:
                cell_line += 'S '
            elif show_start_end and (x, y) == maze.end:
                cell_line += 'E '
            elif path and (x, y) in path_set:
                cell_line += '##'
            else:
                cell_line += '  '
            
            # 右墙
            if cell.has_wall(Direction.EAST):
                cell_line += '|'
            else:
                cell_line += ' '
        
        lines.append(cell_line)
        
        # 墙壁行
        wall_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            # 下墙
            if cell.has_wall(Direction.SOUTH):
                wall_line += '--'
            else:
                wall_line += '  '
            
            wall_line += '+'
        
        lines.append(wall_line)
    
    return '\n'.join(lines)


def render_unicode(maze: Maze, path: Optional[Path] = None,
                   show_start_end: bool = True,
                   style: str = 'box') -> str:
    """
    将迷宫渲染为Unicode字符
    
    使用Unicode Box Drawing字符，更美观
    
    Args:
        maze: 迷宫对象
        path: 可选的路径列表
        show_start_end: 是否显示起点和终点标记
        style: 样式 ('box', 'double', 'round')
        
    Returns:
        Unicode字符串表示
    """
    path_set = set(path) if path else set()
    
    # 根据样式选择字符
    if style == 'double':
        chars = {
            'h': '═', 'v': '║',  # 水平/垂直
            'tl': '╔', 'tr': '╗', 'bl': '╚', 'br': '╝',  # 四角
            'lt': '╠', 'rt': '╣', 'tt': '╦', 'bt': '╩',  # T型
            'cross': '╬',  # 十字
            'space': ' ',
        }
    elif style == 'round':
        chars = {
            'h': '─', 'v': '│',
            'tl': '╭', 'tr': '╮', 'bl': '╰', 'br': '╯',
            'lt': '├', 'rt': '┤', 'tt': '┬', 'bt': '┴',
            'cross': '┼',
            'space': ' ',
        }
    else:  # 'box'
        chars = {
            'h': '─', 'v': '│',
            'tl': '┌', 'tr': '┐', 'bl': '└', 'br': '┘',
            'lt': '├', 'rt': '┤', 'tt': '┬', 'bt': '┴',
            'cross': '┼',
            'space': ' ',
        }
    
    lines = []
    
    # 顶部边界
    top_line = chars['tl']
    for x in range(maze.width):
        top_line += chars['h'] * 2
        if x < maze.width - 1:
            top_line += chars['tt']
        else:
            top_line += chars['tr']
    lines.append(top_line)
    
    for y in range(maze.height):
        # 单元格行
        cell_line = chars['v']
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            # 单元格内容
            if show_start_end and (x, y) == maze.start:
                cell_line += '🚩' if path else 'S '
            elif show_start_end and (x, y) == maze.end:
                cell_line += '🏁' if path else 'E '
            elif path and (x, y) in path_set:
                cell_line += '●●'
            else:
                cell_line += chars['space'] * 2
            
            # 右墙
            if cell.has_wall(Direction.EAST):
                cell_line += chars['v']
            else:
                cell_line += chars['space']
        
        lines.append(cell_line)
        
        # 墙壁行
        wall_line = chars['lt'] if y < maze.height - 1 else chars['bl']
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            # 下墙
            if cell.has_wall(Direction.SOUTH):
                wall_line += chars['h'] * 2
            else:
                wall_line += chars['space'] * 2
            
            # 角落/连接点
            if x < maze.width - 1:
                next_cell = maze.get_cell(x + 1, y)
                if y < maze.height - 1:
                    below_cell = maze.get_cell(x, y + 1)
                    # 判断连接点类型
                    has_h = cell.has_wall(Direction.SOUTH) or below_cell.has_wall(Direction.NORTH)
                    has_v = cell.has_wall(Direction.EAST) or next_cell.has_wall(Direction.WEST)
                    if has_h and has_v:
                        wall_line += chars['cross']
                    elif has_h:
                        wall_line += chars['tt'] if y < maze.height - 1 else chars['bt']
                    elif has_v:
                        wall_line += chars['lt'] if y < maze.height - 1 else chars['rt']
                    else:
                        wall_line += chars['space']
                else:
                    # 最后一行
                    if cell.has_wall(Direction.EAST) or next_cell.has_wall(Direction.WEST):
                        wall_line += chars['bt']
                    else:
                        wall_line += chars['space']
            else:
                wall_line += chars['rt'] if y < maze.height - 1 else chars['br']
        
        lines.append(wall_line)
    
    return '\n'.join(lines)


def render_path(maze: Maze, path: Path,
                path_char: str = '●',
                start_char: str = 'S',
                end_char: str = 'E') -> str:
    """
    渲染带路径标记的迷宫
    
    Args:
        maze: 迷宫对象
        path: 路径列表
        path_char: 路径字符
        start_char: 起点字符
        end_char: 终点字符
        
    Returns:
        渲染后的字符串
    """
    path_set = set(path)
    path_dict = {pos: i for i, pos in enumerate(path)}
    
    lines = []
    
    # 顶部边界
    top_line = '+'
    for x in range(maze.width):
        top_line += '--+'
    lines.append(top_line)
    
    for y in range(maze.height):
        cell_line = '|'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            if (x, y) == path[0]:
                cell_line += start_char + ' '
            elif (x, y) == path[-1]:
                cell_line += end_char + ' '
            elif (x, y) in path_set:
                # 根据路径位置显示数字或符号
                idx = path_dict[(x, y)]
                if idx % 10 < 10:
                    cell_line += path_char + ' '
                else:
                    cell_line += path_char + path_char
            else:
                cell_line += '  '
            
            if cell.has_wall(Direction.EAST):
                cell_line += '|'
            else:
                cell_line += ' '
        
        lines.append(cell_line)
        
        wall_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if cell.has_wall(Direction.SOUTH):
                wall_line += '--'
            else:
                wall_line += '  '
            wall_line += '+'
        
        lines.append(wall_line)
    
    return '\n'.join(lines)


def render_solution_animation(maze: Maze, path: Path) -> List[str]:
    """
    生成解决方案的动画帧序列
    
    每一帧显示路径探索到该点的状态
    
    Args:
        maze: 迷宫对象
        path: 解决方案路径
        
    Returns:
        字符串列表，每帧一个字符串
    """
    frames = []
    for i in range(1, len(path) + 1):
        current_path = path[:i]
        frame = render_unicode(maze, current_path)
        frames.append(frame)
    return frames


def render_heatmap(maze: Maze, distances: dict) -> str:
    """
    渲染距离热力图
    
    Args:
        maze: 迷宫对象
        distances: 位置到距离的映射
        
    Returns:
        热力图字符串
    """
    if not distances:
        return render_ascii(maze)
    
    max_dist = max(distances.values()) if distances else 1
    if max_dist == 0:
        max_dist = 1
    
    # 使用数字或符号表示距离
    heat_chars = ' ░▒▓█'
    
    lines = []
    
    # 顶部边界
    top_line = '+'
    for x in range(maze.width):
        top_line += '--+'
    lines.append(top_line)
    
    for y in range(maze.height):
        cell_line = '|'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            
            if (x, y) in distances:
                dist = distances[(x, y)]
                ratio = dist / max_dist
                if ratio < 0.2:
                    cell_line += '  '
                elif ratio < 0.4:
                    cell_line += '░░'
                elif ratio < 0.6:
                    cell_line += '▒▒'
                elif ratio < 0.8:
                    cell_line += '▓▓'
                else:
                    cell_line += '██'
            else:
                cell_line += '??'
            
            if cell.has_wall(Direction.EAST):
                cell_line += '|'
            else:
                cell_line += ' '
        
        lines.append(cell_line)
        
        wall_line = '+'
        for x in range(maze.width):
            cell = maze.get_cell(x, y)
            if cell.has_wall(Direction.SOUTH):
                wall_line += '--'
            else:
                wall_line += '  '
            wall_line += '+'
        
        lines.append(wall_line)
    
    return '\n'.join(lines)