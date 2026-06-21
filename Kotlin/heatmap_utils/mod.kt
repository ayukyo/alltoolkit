package heatmap_utils

/**
 * Heatmap Utilities (Kotlin)
 * =========================
 *
 * A pure-JVM library for rendering 2D numeric data as terminal-friendly
 * heatmaps using Unicode block characters. Zero external dependencies.
 *
 * # Features
 * - Eight-level Unicode block palette (▁▂▃▄▅▆▇█)
 * - Custom palette support (any CharSequence of ≥ 2 distinct chars)
 * - Configurable aggregation: sum, avg, min, max
 * - Min/max normalization (with optional manual scale)
 * - Row/column labels (left/right/top/bottom)
 * - Border rendering (Unicode box-drawing characters)
 * - Cell annotations for sparse overlays
 * - Heatmap statistics (range, mean, median, std-dev)
 * - CSV/TSV parser to load tabular numeric data
 * - Inversion & contrast controls
 *
 * @author AllToolkit
 * @since 0.1.0
 */
object HeatmapUtils {

    /** Default eight-step block-character palette (low → high density). */
    val DEFAULT_PALETTE: List<String> = listOf(
        " ", "▁", "▂", "▃", "▄", "▅", "▆", "▇", "█"
    )

    /** Smaller seven-step palette without the empty slot. */
    val COMPACT_PALETTE: List<String> = listOf(
        "░", "▒", "▓", "█"
    )

    // =========================================================================
    // Aggregation modes
    // =========================================================================

    enum class Aggregation { SUM, AVG, MIN, MAX }

    // =========================================================================
    // Configuration
    // =========================================================================

    data class HeatmapConfig(
        val palette: List<String> = DEFAULT_PALETTE,
        val aggregation: Aggregation = Aggregation.AVG,
        val invert: Boolean = false,
        val manualMin: Double? = null,
        val manualMax: Double? = null,
        val rowLabels: List<String>? = null,
        val colLabels: List<String>? = null,
        val border: Boolean = true,
        val annotation: (row: Int, col: Int) -> String? = { _, _ -> null }
    ) {
        init {
            require(palette.size >= 2) { "palette must contain at least 2 characters" }
        }
    }

    // =========================================================================
    // Core render
    // =========================================================================

    /**
     * Render a 2D numeric matrix as a heatmap string.
     *
     * @param data rows of numeric values
     * @param config rendering configuration
     * @return the rendered heatmap as a multi-line string
     */
    @JvmStatic
    @JvmOverloads
    fun render(data: List<List<Double>>, config: HeatmapConfig = HeatmapConfig()): String {
        require(data.isNotEmpty()) { "data must not be empty" }
        require(data.all { it.size == data[0].size }) { "all rows must have the same width" }

        val width = data[0].size
        val height = data.size

        // Compute statistics
        val stats = statistics(data)
        val lo = config.manualMin ?: stats.min
        val hi = config.manualMax ?: stats.max
        require(hi >= lo) { "manualMax ($hi) must be >= manualMin ($lo)" }
        val range = (hi - lo).takeIf { it > 0.0 } ?: 1.0

        val sb = StringBuilder()

        // Top column labels
        if (config.colLabels != null) {
            sb.append(columnHeader(width, config.rowLabels, config.colLabels))
        }

        for (r in 0 until height) {
            // Left border
            if (config.border) sb.append('│')
            // Row label
            if (config.rowLabels != null) {
                sb.append(formatLabel(config.rowLabels, r))
            }
            // Cells
            for (c in 0 until width) {
                val v = data[r][c]
                val normalized = ((v - lo) / range).coerceIn(0.0, 1.0)
                val index = paletteIndex(normalized, config)
                sb.append(config.palette[index])
                // Annotation overlay (sparse)
                val annotation = config.annotation(r, c)
                if (annotation != null) {
                    sb.append(annotation)
                }
            }
            // Right row label
            if (config.rowLabels != null) {
                sb.append(formatLabel(config.rowLabels, r))
            }
            // Right border
            if (config.border) sb.append('│')
            sb.append('\n')
        }

        // Bottom column labels
        if (config.colLabels != null && config.border) {
            sb.append(bottomFooter(width, config.rowLabels))
        }

        return sb.toString()
    }

    private fun paletteIndex(normalized: Double, config: HeatmapConfig): Int {
        val steps = config.palette.size
        // Map [0, 1] into palette bins
        val scaled = normalized * (steps - 1)
        val raw = if (config.invert) (steps - 1 - scaled.toInt()) else scaled.toInt()
        return raw.coerceIn(0, steps - 1)
    }

    private fun formatLabel(labels: List<String>, index: Int): String {
        val label = labels.getOrNull(index) ?: ""
        return label.padEnd(3)
    }

    private fun columnHeader(width: Int, rowLabels: List<String>?, colLabels: List<String>): String {
        val sb = StringBuilder()
        if (rowLabels != null) sb.append(" ".repeat(3))
        for (c in 0 until width) {
            val label = colLabels.getOrNull(c) ?: c.toString()
            sb.append(label.take(1))
        }
        sb.append('\n')
        return sb.toString()
    }

    private fun bottomFooter(width: Int, rowLabels: List<String>?): String {
        val sb = StringBuilder()
        if (rowLabels != null) sb.append(" ".repeat(3))
        sb.append('└')
        for (i in 0 until width) sb.append('─')
        sb.append('┘')
        sb.append('\n')
        return sb.toString()
    }

    // =========================================================================
    // Aggregation across multiple layers
    // =========================================================================

    /**
     * Reduce a list of matrices into a single matrix using the configured
     * aggregation mode.
     *
     * @throws IllegalArgumentException if matrices have inconsistent shapes
     */
    @JvmStatic
    fun aggregate(layers: List<List<List<Double>>>, mode: Aggregation): List<List<Double>> {
        require(layers.isNotEmpty()) { "layers must not be empty" }
        val height = layers[0].size
        val width = layers[0][0].size
        require(layers.all { it.size == height && it.all { row -> row.size == width } }) {
            "all layers must have the same shape"
        }
        val result = List(height) { r ->
            List(width) { c ->
                val cell = layers.map { it[r][c] }
                when (mode) {
                    Aggregation.SUM -> cell.sum()
                    Aggregation.AVG -> cell.average()
                    Aggregation.MIN -> cell.min()
                    Aggregation.MAX -> cell.max()
                }
            }
        }
        return result
    }

    // =========================================================================
    // Statistics
    // =========================================================================

    data class Stats(val min: Double, val max: Double, val mean: Double, val median: Double, val stdDev: Double)

    /**
     * Compute descriptive statistics for the matrix.
     */
    @JvmStatic
    fun statistics(data: List<List<Double>>): Stats {
        val flat = data.flatten()
        require(flat.isNotEmpty()) { "data must not be empty" }
        val sorted = flat.sorted()
        val min = sorted.first()
        val max = sorted.last()
        val mean = sorted.average()
        val median = if (sorted.size % 2 == 1) {
            sorted[sorted.size / 2]
        } else {
            (sorted[sorted.size / 2 - 1] + sorted[sorted.size / 2]) / 2.0
        }
        val variance = sorted.map { (it - mean).let { d -> d * d } }.average()
        val stdDev = kotlin.math.sqrt(variance)
        return Stats(min, max, mean, median, stdDev)
    }

    // =========================================================================
    // Inversion & contrast
    // =========================================================================

    /**
     * Invert heatmap intensity by reversing the palette order.
     */
    @JvmStatic
    fun invert(palette: List<String>): List<String> = palette.reversed()

    /**
     * Stretch contrast by clipping values outside [low, high] quantiles.
     */
    @JvmStatic
    fun contrastStretch(data: List<List<Double>>, lowQuantile: Double, highQuantile: Double): List<List<Double>> {
        require(lowQuantile in 0.0..1.0 && highQuantile in 0.0..1.0 && lowQuantile < highQuantile) {
            "quantiles must satisfy 0 <= low < high <= 1"
        }
        val flat = data.flatten().sorted()
        val n = flat.size
        val lo = flat[(lowQuantile * (n - 1)).toInt().coerceIn(0, n - 1)]
        val hi = flat[(highQuantile * (n - 1)).toInt().coerceIn(0, n - 1)]
        val range = (hi - lo).takeIf { it > 0.0 } ?: 1.0
        return data.map { row ->
            row.map { v ->
                ((v - lo) / range).coerceIn(0.0, 1.0)
            }
        }
    }

    // =========================================================================
    // Parsers
    // =========================================================================

    /**
     * Parse CSV/TSV text into a 2D numeric matrix.
     *
     * - First non-numeric row is treated as column labels (if all cells parse).
     * - First column of subsequent rows is treated as row labels (if non-numeric).
     *
     * @return Pair(matrix, optional labels)
     */
    @JvmStatic
    fun parseDelimited(
        text: String,
        delimiter: Char = ',',
        hasColumnLabels: Boolean = false,
        hasRowLabels: Boolean = false
    ): Triple<List<List<Double>>, List<String>?, List<String>?> {
        val lines = text.lines().filter { it.isNotBlank() }
        require(lines.isNotEmpty()) { "input must not be empty" }

        var startIdx = 0
        var colLabels: List<String>? = null
        var rowLabels: MutableList<String>? = null

        if (hasColumnLabels) {
            val header = lines[0].split(delimiter).map { it.trim() }
            val firstDataIdx = if (hasRowLabels) 1 else 0
            colLabels = if (hasRowLabels) header.drop(firstDataIdx) else header
            startIdx = 1
        }
        if (hasRowLabels) {
            rowLabels = mutableListOf()
        }

        val rows = mutableListOf<List<Double>>()
        for (i in startIdx until lines.size) {
            val cells = lines[i].split(delimiter).map { it.trim() }
            var cellStart = 0
            if (hasRowLabels) {
                rowLabels!!.add(cells[0])
                cellStart = 1
            }
            val row = cells.drop(cellStart).map { it.toDouble() }
            rows.add(row)
        }
        return Triple(rows, rowLabels?.toList(), colLabels)
    }

    // =========================================================================
    // Example program
    // =========================================================================

    @JvmStatic
    fun example() {
        val matrix = listOf(
            listOf(1.0, 2.0, 3.0, 4.0),
            listOf(5.0, 6.0, 7.0, 8.0),
            listOf(9.0, 10.0, 11.0, 12.0),
            listOf(13.0, 14.0, 15.0, 16.0)
        )
        val config = HeatmapConfig(
            rowLabels = listOf("A", "B", "C", "D"),
            colLabels = listOf("1", "2", "3", "4")
        )
        println(render(matrix, config))
    }
}