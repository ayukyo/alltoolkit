package heatmap_utils

/**
 * HeatmapUtils Test Suite
 *
 * Run with:
 *   kotlinc mod.kt heatmap_utils_test.kt -include-runtime -d heatmap_utils_test.jar \
 *     && java -jar heatmap_utils_test.jar
 */
fun main() {
    println("Running HeatmapUtils Tests...")
    println("=".repeat(60))

    var passed = 0
    var failed = 0

    fun run(name: String, block: () -> Unit) {
        try {
            block()
            println("PASSED: $name")
            passed++
        } catch (e: Throwable) {
            println("FAILED: $name - ${e.message}")
            failed++
        }
    }

    // 1. Basic render produces correct number of lines
    run("Basic render produces correct number of lines") {
        val matrix = listOf(
            listOf(1.0, 2.0, 3.0),
            listOf(4.0, 5.0, 6.0),
            listOf(7.0, 8.0, 9.0)
        )
        val out = HeatmapUtils.render(matrix)
        assert(out.lines().size == 3) { "expected 3 lines, got ${out.lines().size}" }
    }

    // 2. Render with row labels includes labels in output
    run("Render with row labels includes labels") {
        val matrix = listOf(
            listOf(1.0, 2.0),
            listOf(3.0, 4.0)
        )
        val config = HeatmapUtils.HeatmapConfig(rowLabels = listOf("R1", "R2"))
        val out = HeatmapUtils.render(matrix, config)
        assert(out.contains("R1")) { "output should contain R1" }
        assert(out.contains("R2")) { "output should contain R2" }
    }

    // 3. Min value gets the lowest palette character (or low slot)
    run("Min value maps to lowest palette slot") {
        val matrix = listOf(
            listOf(0.0, 1.0),
            listOf(1.0, 1.0)
        )
        val out = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false))
        val lines = out.lines()
        val firstChar = lines[0][0]
        // DEFAULT_PALETTE[0] is " " (a space). normalized 0 → index 0 → " "
        assert(firstChar == ' ' || firstChar.toString() == HeatmapUtils.DEFAULT_PALETTE[0]) {
            "expected space for min, got '$firstChar'"
        }
    }

    // 4. Max value gets the highest palette character
    run("Max value maps to highest palette slot") {
        val matrix = listOf(
            listOf(0.0, 1.0)
        )
        val out = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false))
        val lines = out.lines()
        val lastChar = lines[0][1]
        val expected = HeatmapUtils.DEFAULT_PALETTE.last()
        assert(lastChar.toString() == expected) {
            "expected '$expected' for max, got '$lastChar'"
        }
    }

    // 5. Inversion flips the palette mapping
    run("Inversion flips min/max characters") {
        val matrix = listOf(
            listOf(0.0, 1.0)
        )
        val normal = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false))
        val inverted = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false, invert = true))
        val nLines = normal.lines()
        val iLines = inverted.lines()
        assert(nLines[0][0] != iLines[0][0] || normal != inverted) {
            "inverted output should differ from normal output"
        }
    }

    // 6. Border toggles left/right borders
    run("Border adds left edge character") {
        val matrix = listOf(listOf(1.0))
        val withBorder = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = true))
        val withoutBorder = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false))
        assert(withBorder.contains('│')) { "expected '│' in bordered output" }
        assert(!withoutBorder.contains('│')) { "expected no '│' without border" }
    }

    // 7. Aggregation SUM
    run("Aggregation SUM sums layer cells") {
        val layers = listOf(
            listOf(listOf(1.0, 2.0), listOf(3.0, 4.0)),
            listOf(listOf(10.0, 20.0), listOf(30.0, 40.0))
        )
        val result = HeatmapUtils.aggregate(layers, HeatmapUtils.Aggregation.SUM)
        assert(result[0][0] == 11.0) { "expected 11.0, got ${result[0][0]}" }
        assert(result[1][1] == 44.0) { "expected 44.0, got ${result[1][1]}" }
    }

    // 8. Aggregation AVG
    run("Aggregation AVG averages layer cells") {
        val layers = listOf(
            listOf(listOf(2.0, 4.0)),
            listOf(listOf(6.0, 8.0))
        )
        val result = HeatmapUtils.aggregate(layers, HeatmapUtils.Aggregation.AVG)
        assert(result[0][0] == 4.0) { "expected 4.0, got ${result[0][0]}" }
        assert(result[0][1] == 6.0) { "expected 6.0, got ${result[0][1]}" }
    }

    // 9. Aggregation MIN/MAX
    run("Aggregation MIN and MAX") {
        val layers = listOf(
            listOf(listOf(5.0, 1.0)),
            listOf(listOf(2.0, 9.0))
        )
        val minResult = HeatmapUtils.aggregate(layers, HeatmapUtils.Aggregation.MIN)
        val maxResult = HeatmapUtils.aggregate(layers, HeatmapUtils.Aggregation.MAX)
        assert(minResult[0][0] == 2.0 && minResult[0][1] == 1.0) {
            "MIN failed: ${minResult[0]}"
        }
        assert(maxResult[0][0] == 5.0 && maxResult[0][1] == 9.0) {
            "MAX failed: ${maxResult[0]}"
        }
    }

    // 10. Statistics compute correct min/max/mean
    run("Statistics: min/max/mean") {
        val data = listOf(
            listOf(1.0, 2.0, 3.0),
            listOf(4.0, 5.0, 6.0)
        )
        val stats = HeatmapUtils.statistics(data)
        assert(stats.min == 1.0) { "min: ${stats.min}" }
        assert(stats.max == 6.0) { "max: ${stats.max}" }
        assert(kotlin.math.abs(stats.mean - 3.5) < 1e-9) { "mean: ${stats.mean}" }
    }

    // 11. Median for odd-length flat sequence
    run("Median: odd count") {
        val data = listOf(listOf(1.0, 2.0, 3.0))
        val stats = HeatmapUtils.statistics(data)
        assert(stats.median == 2.0) { "median: ${stats.median}" }
    }

    // 12. Median for even-length flat sequence
    run("Median: even count") {
        val data = listOf(listOf(1.0, 2.0, 3.0, 4.0))
        val stats = HeatmapUtils.statistics(data)
        assert(stats.median == 2.5) { "median: ${stats.median}" }
    }

    // 13. Std-dev for known sample
    run("Std-dev for uniform sample") {
        val data = listOf(listOf(2.0, 4.0, 4.0, 4.0, 5.0, 5.0, 7.0, 9.0))
        val stats = HeatmapUtils.statistics(data)
        // population std-dev of [2,4,4,4,5,5,7,9] is sqrt(32/8)=2.0
        assert(kotlin.math.abs(stats.stdDev - 2.0) < 1e-9) {
            "std-dev: ${stats.stdDev} (expected ~2.0)"
        }
    }

    // 14. invert() reverses the palette
    run("invert() reverses palette") {
        val p = listOf("a", "b", "c")
        val inv = HeatmapUtils.invert(p)
        assert(inv == listOf("c", "b", "a")) { "invert result: $inv" }
    }

    // 15. contrastStretch clamps to [0,1]
    run("contrastStretch clamps output to [0,1]") {
        val data = listOf(
            listOf(-10.0, 0.0, 5.0),
            listOf(10.0, 100.0, 50.0)
        )
        val stretched = HeatmapUtils.contrastStretch(data, 0.1, 0.9)
        for (row in stretched) {
            for (v in row) {
                assert(v in 0.0..1.0) { "value out of range: $v" }
            }
        }
    }

    // 16. contrastStretch with extreme quantiles leaves only 0/1
    run("contrastStretch extremes produce 0 and 1 only") {
        val data = listOf(listOf(1.0, 2.0, 3.0, 4.0, 5.0))
        val stretched = HeatmapUtils.contrastStretch(data, 0.0, 1.0)
        assert(stretched[0][0] == 0.0) { "first should be 0" }
        assert(stretched[0][4] == 1.0) { "last should be 1" }
    }

    // 17. parseDelimited: CSV with no labels
    run("parseDelimited: CSV basic") {
        val csv = "1,2,3\n4,5,6\n7,8,9"
        val (rows, _, _) = HeatmapUtils.parseDelimited(csv, ',', false, false)
        assert(rows.size == 3) { "row count: ${rows.size}" }
        assert(rows[0] == listOf(1.0, 2.0, 3.0)) { "row 0: ${rows[0]}" }
        assert(rows[2] == listOf(7.0, 8.0, 9.0)) { "row 2: ${rows[2]}" }
    }

    // 18. parseDelimited: TSV with row + column labels
    run("parseDelimited: TSV with row/col labels") {
        val tsv = "X\tA\tB\tC\nR1\t1\t2\t3\nR2\t4\t5\t6"
        val (rows, rowLabels, colLabels) = HeatmapUtils.parseDelimited(tsv, '\t', true, true)
        assert(rows.size == 2) { "row count: ${rows.size}" }
        assert(rowLabels == listOf("R1", "R2")) { "row labels: $rowLabels" }
        assert(colLabels == listOf("A", "B", "C")) { "col labels: $colLabels" }
        assert(rows[1] == listOf(4.0, 5.0, 6.0)) { "row 2 values: ${rows[1]}" }
    }

    // 19. Empty matrix is rejected
    run("Empty matrix is rejected") {
        var threw = false
        try {
            HeatmapUtils.render(emptyList())
        } catch (e: IllegalArgumentException) {
            threw = true
        }
        assert(threw) { "expected IllegalArgumentException for empty data" }
    }

    // 20. Ragged matrix is rejected
    run("Ragged matrix is rejected") {
        var threw = false
        try {
            HeatmapUtils.render(listOf(listOf(1.0), listOf(1.0, 2.0)))
        } catch (e: IllegalArgumentException) {
            threw = true
        }
        assert(threw) { "expected IllegalArgumentException for ragged rows" }
    }

    // 21. Custom palette is honored
    run("Custom palette produces custom chars") {
        val matrix = listOf(listOf(0.0, 1.0))
        val config = HeatmapUtils.HeatmapConfig(palette = listOf("L", "H"), border = false)
        val out = HeatmapUtils.render(matrix, config)
        val line = out.lines()[0]
        assert(line[0] == 'L') { "first cell should be L, got '${line[0]}'" }
        assert(line[1] == 'H') { "second cell should be H, got '${line[1]}'" }
    }

    // 22. Compact palette renders correctly
    run("Compact palette rendering") {
        val matrix = listOf(listOf(0.0, 0.5, 1.0))
        val config = HeatmapUtils.HeatmapConfig(palette = HeatmapUtils.COMPACT_PALETTE, border = false)
        val out = HeatmapUtils.render(matrix, config)
        val line = out.lines()[0]
        assert(line[0].toString() == HeatmapUtils.COMPACT_PALETTE.first()) {
            "first should be '${HeatmapUtils.COMPACT_PALETTE.first()}'"
        }
        assert(line[2].toString() == HeatmapUtils.COMPACT_PALETTE.last()) {
            "last should be '${HeatmapUtils.COMPACT_PALETTE.last()}'"
        }
    }

    // 23. Manual min/max override
    run("Manual min/max override clamps normalization") {
        val matrix = listOf(listOf(-100.0, 0.0, 100.0))
        val config = HeatmapUtils.HeatmapConfig(
            border = false,
            manualMin = 0.0,
            manualMax = 10.0
        )
        val out = HeatmapUtils.render(matrix, config)
        val line = out.lines()[0]
        // -100 < 0.0 → clamps to 0.0 → palette[0] = ' '
        assert(line[0] == ' ') { "manualMin clamp: first cell should be space, got '${line[0]}'" }
        // 100 > 10.0 → clamps to 1.0 → palette[last] = '█'
        assert(line[2].toString() == HeatmapUtils.DEFAULT_PALETTE.last()) {
            "manualMax clamp: last cell should be ${HeatmapUtils.DEFAULT_PALETTE.last()}"
        }
    }

    // 24. Annotation callback injects extra characters
    run("Annotation callback injects extra characters") {
        val matrix = listOf(
            listOf(1.0, 2.0),
            listOf(3.0, 4.0)
        )
        val config = HeatmapUtils.HeatmapConfig(
            border = false,
            annotation = { r: Int, c: Int -> if (r == 0 && c == 1) "*" else null }
        )
        val out = HeatmapUtils.render(matrix, config)
        assert(out.contains("*")) { "annotation '*' should appear in output" }
    }

    // 25. Aggregation rejects inconsistent shapes
    run("Aggregation rejects inconsistent shapes") {
        var threw = false
        try {
            HeatmapUtils.aggregate(
                listOf(
                    listOf(listOf(1.0, 2.0)),
                    listOf(listOf(1.0))
                ),
                HeatmapUtils.Aggregation.SUM
            )
        } catch (e: IllegalArgumentException) {
            threw = true
        }
        assert(threw) { "expected IllegalArgumentException for inconsistent shapes" }
    }

    // 26. Single-cell matrix renders one cell
    run("Single-cell matrix renders one cell") {
        val out = HeatmapUtils.render(listOf(listOf(42.0)), HeatmapUtils.HeatmapConfig(border = false))
        val lines = out.lines()
        assert(lines.size == 1) { "expected 1 line, got ${lines.size}" }
        assert(lines[0].length == 1) { "expected length 1, got ${lines[0].length}" }
    }

    // 27. Default palette has 9 steps
    run("Default palette has 9 entries") {
        assert(HeatmapUtils.DEFAULT_PALETTE.size == 9) {
            "expected 9 entries, got ${HeatmapUtils.DEFAULT_PALETTE.size}"
        }
    }

    // 28. Parse delimited with only column labels
    run("parseDelimited: column labels only") {
        val csv = "A,B,C\n1,2,3"
        val (rows, rowLabels, colLabels) = HeatmapUtils.parseDelimited(csv, ',', true, false)
        assert(rows.size == 1) { "expected 1 data row, got ${rows.size}" }
        assert(rowLabels == null) { "rowLabels should be null" }
        assert(colLabels == listOf("A", "B", "C")) { "col labels: $colLabels" }
    }

    // 29. Heatmap with large matrix produces correct line count
    run("Heatmap line count matches matrix height") {
        val matrix = (0 until 10).map { r -> (0 until 5).map { c -> (r * 5 + c).toDouble() } }
        val out = HeatmapUtils.render(matrix, HeatmapUtils.HeatmapConfig(border = false))
        assert(out.lines().size == 10) {
            "expected 10 lines, got ${out.lines().size}"
        }
    }

    // 30. Row label padding is consistent
    run("Row labels are padded to width 3") {
        val matrix = listOf(listOf(1.0))
        val config = HeatmapUtils.HeatmapConfig(rowLabels = listOf("X"), border = false)
        val out = HeatmapUtils.render(matrix, config)
        // "X  " padded to 3 chars precedes the single cell
        val lines = out.lines()
        assert(lines[0].startsWith("X  ")) {
            "expected line to start with 'X  ', got '${lines[0]}'"
        }
    }

    println("=".repeat(60))
    println("Tests completed: $passed passed, $failed failed")

    if (failed > 0) {
        kotlin.system.exitProcess(1)
    }
}