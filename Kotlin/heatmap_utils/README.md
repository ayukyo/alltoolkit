# heatmap_utils (Kotlin)

Render 2D numeric data as terminal-friendly heatmaps using Unicode block
characters. Pure JVM, zero external dependencies.

## Features

- **Block-character palettes** (default 9-step `▁▂▃▄▅▆▇█`, compact 4-step
  `░▒▓█`, fully custom).
- **Layer aggregation** — combine multiple matrices with `SUM`, `AVG`,
  `MIN`, or `MAX`.
- **Statistics** — `min`, `max`, `mean`, `median`, population `std-dev`.
- **Normalization** — auto range, manual `manualMin`/`manualMax`, or
  `contrastStretch()` with quantile clipping.
- **Inversion** — flip the palette mapping.
- **Annotations** — inject per-cell markers via callback.
- **Borders** — Unicode box-drawing characters.
- **CSV/TSV parser** — load delimited data with optional row/column labels.
- **Zero dependencies** — only the Kotlin/Java standard library.

## Quick start

```kotlin
import heatmap_utils.HeatmapUtils

val matrix = listOf(
    listOf(1.0,  2.0,  3.0,  4.0),
    listOf(5.0,  6.0,  7.0,  8.0),
    listOf(9.0, 10.0, 11.0, 12.0),
    listOf(13.0, 14.0, 15.0, 16.0)
)

val config = HeatmapUtils.HeatmapConfig(
    rowLabels = listOf("A", "B", "C", "D"),
    colLabels = listOf("1", "2", "3", "4")
)
println(HeatmapUtils.render(matrix, config))
```

## Output

```
   1234
│A    ▁▁A  │
│B  ▂▂▃▃B  │
│C  ▄▄▅▅C  │
│D  ▆▆▇█D  │
   └────┘
```

## API

### `HeatmapUtils.render(data, config)`
Render a `List<List<Double>>` matrix to a multi-line heatmap string.

### `HeatmapUtils.aggregate(layers, mode)`
Reduce a `List<List<List<Double>>>` of layers to a single matrix using one
of `Aggregation.SUM` / `AVG` / `MIN` / `MAX`.

### `HeatmapUtils.statistics(data)`
Returns a `Stats(min, max, mean, median, stdDev)` value.

### `HeatmapUtils.contrastStretch(data, lowQuantile, highQuantile)`
Clips values to a quantile range and rescales into `[0, 1]`.

### `HeatmapUtils.parseDelimited(text, delimiter, hasColumnLabels, hasRowLabels)`
Parses CSV/TSV text into a numeric matrix plus optional row/column labels.

## Building & Testing

```bash
cd Kotlin/heatmap_utils
kotlinc mod.kt heatmap_utils_test.kt -include-runtime -d heatmap_utils_test.jar
java -jar heatmap_utils_test.jar
```

The test suite contains **30 tests** covering rendering, palettes,
aggregation, statistics, parsing, inversion, contrast stretching, border
configuration, and error paths. All tests pass with Kotlin 2.3+ on JRE 17+.

## License

MIT — AllToolkit contributors.