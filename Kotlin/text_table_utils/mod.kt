/**
 * Text Table Utils - 文本表格生成工具
 * 
 * 支持 ASCII、Markdown、HTML 格式的表格渲染
 * 零外部依赖，纯 Kotlin 标准库实现
 * 
 * @author AllToolkit
 * @date 2026-05-03
 */

package text_table_utils

/**
 * 表格对齐方式
 */
enum class Alignment {
    LEFT,
    CENTER,
    RIGHT
}

/**
 * 表格列配置
 */
data class Column(
    val title: String,
    val width: Int = 0, // 0 表示自动宽度
    val alignment: Alignment = Alignment.LEFT
)

/**
 * 文本表格类
 */
class TextTable(
    private val columns: List<Column>,
    private val rows: List<List<String>> = emptyList()
) {
    private val _rows = rows.toMutableList()
    
    /**
     * 添加一行数据
     */
    fun addRow(vararg values: String): TextTable {
        _rows.add(values.toList())
        return this
    }
    
    /**
     * 添加多行数据
     */
    fun addRows(newRows: List<List<String>>): TextTable {
        _rows.addAll(newRows)
        return this
    }
    
    /**
     * 获取所有行
     */
    fun getRows(): List<List<String>> = _rows.toList()
    
    /**
     * 计算列宽
     */
    private fun calculateColumnWidths(): List<Int> {
        return columns.mapIndexed { index, column ->
            val titleWidth = column.title.length
            val contentWidth = if (_rows.isEmpty()) 0 else _rows.maxOfOrNull { 
                it.getOrElse(index) { "" }.getDisplayLength() 
            } ?: 0
            maxOf(column.width, titleWidth, contentWidth)
        }
    }
    
    /**
     * 获取字符串的显示长度（考虑中文等宽字符）
     */
    private fun String.getDisplayLength(): Int {
        return this.sumOf { char ->
            when {
                char.code < 32 -> 0 // 控制字符
                char.code < 127 -> 1 // ASCII 字符
                else -> 2 // 中文等宽字符
            }
        }
    }
    
    /**
     * 填充字符串到指定长度
     */
    private fun String.padToLength(length: Int, alignment: Alignment): String {
        val displayLen = this.getDisplayLength()
        val padding = length - displayLen
        if (padding <= 0) return this
        
        return when (alignment) {
            Alignment.LEFT -> this + " ".repeat(padding)
            Alignment.RIGHT -> " ".repeat(padding) + this
            Alignment.CENTER -> {
                val leftPad = padding / 2
                val rightPad = padding - leftPad
                " ".repeat(leftPad) + this + " ".repeat(rightPad)
            }
        }
    }
    
    /**
     * 渲染为 ASCII 表格
     */
    fun toAscii(): String {
        val widths = calculateColumnWidths()
        val sb = StringBuilder()
        
        // 顶部边框
        sb.append("+")
        widths.forEach { width ->
            sb.append("-".repeat(width + 2))
            sb.append("+")
        }
        sb.append("\n")
        
        // 表头
        sb.append("|")
        columns.forEachIndexed { index, column ->
            sb.append(" ")
            sb.append(column.title.padToLength(widths[index], Alignment.CENTER))
            sb.append(" |")
        }
        sb.append("\n")
        
        // 表头分隔线
        sb.append("+")
        widths.forEach { width ->
            sb.append("=".repeat(width + 2))
            sb.append("+")
        }
        sb.append("\n")
        
        // 数据行
        _rows.forEach { row ->
            sb.append("|")
            columns.forEachIndexed { index, column ->
                sb.append(" ")
                val value = row.getOrElse(index) { "" }
                sb.append(value.padToLength(widths[index], column.alignment))
                sb.append(" |")
            }
            sb.append("\n")
        }
        
        // 底部边框
        sb.append("+")
        widths.forEach { width ->
            sb.append("-".repeat(width + 2))
            sb.append("+")
        }
        
        return sb.toString()
    }
    
    /**
     * 渲染为 Markdown 表格
     */
    fun toMarkdown(): String {
        val widths = calculateColumnWidths()
        val sb = StringBuilder()
        
        // 表头
        sb.append("|")
        columns.forEachIndexed { index, column ->
            sb.append(" ")
            sb.append(column.title.padToLength(widths[index], Alignment.CENTER))
            sb.append(" |")
        }
        sb.append("\n")
        
        // 对齐分隔线
        sb.append("|")
        columns.forEachIndexed { index, column ->
            val width = widths[index]
            sb.append(" ")
            sb.append(when (column.alignment) {
                Alignment.LEFT -> ":" + "-".repeat(width - 1)
                Alignment.RIGHT -> "-".repeat(width - 1) + ":"
                Alignment.CENTER -> ":" + "-".repeat(width - 2) + ":"
            })
            sb.append(" |")
        }
        sb.append("\n")
        
        // 数据行
        _rows.forEach { row ->
            sb.append("|")
            columns.forEachIndexed { index, column ->
                sb.append(" ")
                val value = row.getOrElse(index) { "" }
                sb.append(value.padToLength(widths[index], column.alignment))
                sb.append(" |")
            }
            sb.append("\n")
        }
        
        return sb.toString().trimEnd()
    }
    
    /**
     * 渲染为 HTML 表格
     */
    fun toHtml(cssClass: String? = null): String {
        val sb = StringBuilder()
        
        val tableClass = if (cssClass != null) """ class="$cssClass"""" else ""
        sb.append("<table$tableClass>\n")
        
        // 表头
        sb.append("  <thead>\n")
        sb.append("    <tr>\n")
        columns.forEach { column ->
            val align = when (column.alignment) {
                Alignment.LEFT -> "left"
                Alignment.CENTER -> "center"
                Alignment.RIGHT -> "right"
            }
            sb.append("""      <th style="text-align: $align">${escapeHtml(column.title)}</th>
""")
        }
        sb.append("    </tr>\n")
        sb.append("  </thead>\n")
        
        // 数据行
        sb.append("  <tbody>\n")
        _rows.forEach { row ->
            sb.append("    <tr>\n")
            columns.forEachIndexed { index, column ->
                val align = when (column.alignment) {
                    Alignment.LEFT -> "left"
                    Alignment.CENTER -> "center"
                    Alignment.RIGHT -> "right"
                }
                val value = row.getOrElse(index) { "" }
                sb.append("""      <td style="text-align: $align">${escapeHtml(value)}</td>
""")
            }
            sb.append("    </tr>\n")
        }
        sb.append("  </tbody>\n")
        sb.append("</table>")
        
        return sb.toString()
    }
    
    /**
     * 转义 HTML 特殊字符
     */
    private fun escapeHtml(text: String): String {
        return text
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace("\"", "&quot;")
            .replace("'", "&#39;")
    }
    
    /**
     * 渲染为简单表格（无边框）
     */
    fun toSimple(): String {
        val widths = calculateColumnWidths()
        val sb = StringBuilder()
        
        // 表头
        columns.forEachIndexed { index, column ->
            if (index > 0) sb.append("  ")
            sb.append(column.title.padToLength(widths[index], Alignment.CENTER))
        }
        sb.append("\n")
        
        // 分隔线
        columns.forEachIndexed { index, _ ->
            if (index > 0) sb.append("  ")
            sb.append("-".repeat(widths[index]))
        }
        sb.append("\n")
        
        // 数据行
        _rows.forEach { row ->
            columns.forEachIndexed { index, column ->
                if (index > 0) sb.append("  ")
                val value = row.getOrElse(index) { "" }
                sb.append(value.padToLength(widths[index], column.alignment))
            }
            sb.append("\n")
        }
        
        return sb.toString().trimEnd()
    }
    
    /**
     * 渲染为 CSV 格式
     */
    fun toCsv(): String {
        val sb = StringBuilder()
        
        // 表头
        sb.append(columns.joinToString(",") { escapeCsv(it.title) })
        sb.append("\n")
        
        // 数据行
        _rows.forEach { row ->
            sb.append(row.indices.joinToString(",") { index ->
                escapeCsv(row.getOrElse(index) { "" })
            })
            sb.append("\n")
        }
        
        return sb.toString().trimEnd()
    }
    
    /**
     * 转义 CSV 字段
     */
    private fun escapeCsv(field: String): String {
        return if (field.contains(",") || field.contains("\"") || field.contains("\n")) {
            "\"${field.replace("\"", "\"\"")}\""
        } else {
            field
        }
    }
    
    /**
     * 渲染为 JSON 格式
     */
    fun toJson(): String {
        val sb = StringBuilder()
        sb.append("[\n")
        
        _rows.forEachIndexed { rowIndex, row ->
            sb.append("  {\n")
            columns.forEachIndexed { colIndex, column ->
                val value = row.getOrElse(colIndex) { "" }
                sb.append("    \"${escapeJson(column.title)}\": \"${escapeJson(value)}\"")
                if (colIndex < columns.size - 1) sb.append(",")
                sb.append("\n")
            }
            sb.append("  }")
            if (rowIndex < _rows.size - 1) sb.append(",")
            sb.append("\n")
        }
        
        sb.append("]")
        return sb.toString()
    }
    
    /**
     * 转义 JSON 字符串
     */
    private fun escapeJson(text: String): String {
        return text
            .replace("\\", "\\\\")
            .replace("\"", "\\\"")
            .replace("\n", "\\n")
            .replace("\r", "\\r")
            .replace("\t", "\\t")
    }
    
    override fun toString(): String = toAscii()
}

/**
 * 表格构建器
 */
class TableBuilder {
    private val columns = mutableListOf<Column>()
    private val rows = mutableListOf<List<String>>()
    
    /**
     * 添加列
     */
    fun column(title: String, width: Int = 0, alignment: Alignment = Alignment.LEFT): TableBuilder {
        columns.add(Column(title, width, alignment))
        return this
    }
    
    /**
     * 添加左对齐列
     */
    fun leftColumn(title: String, width: Int = 0): TableBuilder {
        return column(title, width, Alignment.LEFT)
    }
    
    /**
     * 添加居中对齐列
     */
    fun centerColumn(title: String, width: Int = 0): TableBuilder {
        return column(title, width, Alignment.CENTER)
    }
    
    /**
     * 添加右对齐列
     */
    fun rightColumn(title: String, width: Int = 0): TableBuilder {
        return column(title, width, Alignment.RIGHT)
    }
    
    /**
     * 添加行
     */
    fun row(vararg values: String): TableBuilder {
        rows.add(values.toList())
        return this
    }
    
    /**
     * 从数据列表添加行
     */
    fun rows(data: List<List<String>>): TableBuilder {
        rows.addAll(data)
        return this
    }
    
    /**
     * 构建表格
     */
    fun build(): TextTable {
        return TextTable(columns, rows)
    }
}

/**
 * DSL 函数 - 创建表格
 */
fun table(init: TableBuilder.() -> Unit): TextTable {
    val builder = TableBuilder()
    builder.init()
    return builder.build()
}

/**
 * 快速创建表格
 */
fun quickTable(vararg headers: String): TextTable {
    val columns = headers.map { Column(it) }
    return TextTable(columns)
}

/**
 * 从二维数组创建表格
 */
fun arrayToTable(headers: List<String>, data: List<List<String>>): TextTable {
    val columns = headers.map { Column(it) }
    return TextTable(columns, data)
}

/**
 * 对齐枚举扩展
 */
object Align {
    val LEFT = Alignment.LEFT
    val CENTER = Alignment.CENTER
    val RIGHT = Alignment.RIGHT
}