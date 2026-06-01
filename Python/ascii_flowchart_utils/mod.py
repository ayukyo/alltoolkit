# ASCII Flowchart Utils
# Pure Python 3.6+, zero external dependencies.

"""
ASCII Flowchart Utilities

Supports:
- Box: ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼
- Decision: Diamond shape
- Arrows: → ← ↑ ↓
- 4 styles: box, round, bold, double
- Multi-line node text with auto-wrap
- Fluent API
- Quick helper function
"""

# ─── Glyph Sets ──────────────────────────────────────────────────────────────

GLYPH_BOX = {
    "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
    "v": "│", "h": "─",
    "l": "├", "r": "┤", "t": "┬", "b": "┴", "c": "┼",
}

GLYPH_ROUND = {
    "tl": "/ ", "tr": " \\", "bl": "\\ ", "br": " /",
    "v": "| ", "h": "--",
    "l": "+-", "r": "-+", "t": "-+-", "b": "-+-", "c": "-+-",
}

GLYPH_BOLD = {
    "tl": "┏", "tr": "┓", "bl": "┗", "br": "┛",
    "v": "┃", "h": "━",
    "l": "┣", "r": "┫", "t": "┳", "b": "┻", "c": "╋",
}

GLYPH_DOUBLE = {
    "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
    "v": "║", "h": "═",
    "l": "╠", "r": "╣", "t": "╦", "b": "╩", "c": "╬",
}

STYLE_GLYPHS = {
    "box": GLYPH_BOX,
    "round": GLYPH_ROUND,
    "bold": GLYPH_BOLD,
    "double": GLYPH_DOUBLE,
}

ARROW_RIGHT = "→"
ARROW_LEFT = "←"
ARROW_DOWN = "↓"
ARROW_UP = "↑"

BRANCH_LABELS = {"yes": "Y", "no": "N", "true": "T", "false": "F"}

NODE_CHARS = {
    "terminator": ("( ", " )"),
    "process": ("[ ", " ]"),
    "decision": ("◆ ", " ◆"),
    "data": ("◇ ", " ◇"),
    "preparation": ("/ ", " \\"),
    "manual_input": ("[ ", " ]"),
    "connector": ("○ ", " ○"),
    "off_page": ("◇ ", "⊡"),
}


# ─── Core Builder ──────────────────────────────────────────────────────────────

class Flowchart:
    def __init__(self, style="box", arrow=ARROW_RIGHT, indent=2, min_col_width=10):
        if style not in STYLE_GLYPHS:
            raise ValueError("Unknown style: {!r}. Choose: {!r}".format(style, list(STYLE_GLYPHS)))
        self.g = STYLE_GLYPHS[style]
        self.arrow = arrow
        self.indent = indent
        self.min_col_width = max(min_col_width, 6)
        self.nodes = []

    def add(self, text, node_type="process", label=None):
        self.nodes.append({"text": text, "type": node_type, "label": label})
        return self

    def start(self, text="开始"):
        return self.add(text, "terminator")

    def end(self, text="结束"):
        return self.add(text, "terminator")

    def process(self, text):
        return self.add(text, "process")

    def decision(self, text):
        return self.add(text, "decision")

    def data(self, text):
        return self.add(text, "data")

    def sub(self, text):
        return self.add(text, "preparation")

    def input(self, text):
        return self.add(text, "manual_input")

    def off_page(self, text="下一页"):
        return self.add(text, "off_page")

    def connector(self, text=""):
        return self.add(text, "connector")

    def branch(self, text, left_label="N", right_label="Y"):
        self.add(text, "decision", label="{}/{}".format(left_label, right_label))
        return self

    # ── Text Wrapping ─────────────────────────────────────────────────────────

    def _wrap(self, text, max_w=None):
        if max_w is None:
            max_w = self.min_col_width - 4
        words = text.split()
        lines, cur = [], ""
        for w in words:
            test = (cur + " " + w).strip()
            if len(test) > max_w and cur:
                lines.append(cur)
                cur = w
            else:
                cur = test
        if cur:
            lines.append(cur)
        return lines or [""]

    # ── Single Node Render ────────────────────────────────────────────────────

    def _draw_node(self, node):
        g = self.g
        text = node["text"]
        ntype = node["type"]
        lines = self._wrap(text)
        w = max(len(l) for l in lines)

        if ntype == "decision":
            # Diamond: left-side content, right-side content
            half = (w + 1) // 2
            top = max(0, half - 1)
            bot = max(0, w - half)
            result = []
            content_idx = 0
            for i in range(w):
                content = ""
                if top <= i < top + len(lines):
                    content = lines[content_idx]
                    content_idx += 1
                pad = max(0, w - len(content))
                result.append("{}{}{}{}".format(g["v"], content, " " * pad, g["v"]))
            return result

        open_s, close_s = NODE_CHARS.get(ntype, ("[ ", " ]"))
        bar = g["v"] if ntype not in ("terminator", "connector") else " "
        result = []
        for ln in lines:
            pad = max(0, w - len(ln))
            result.append("{}{}{}{}".format(bar, ln, " " * pad, bar))
        return result

    # ── Horizontal Concatenation ──────────────────────────────────────────────

    def _hconcat(self, left_lines, right_lines, sep=""):
        max_len = max(len(left_lines), len(right_lines))
        result = []
        for i in range(max_len):
            l = left_lines[i] if i < len(left_lines) else " " * len(left_lines[0])
            r = right_lines[i] if i < len(right_lines) else " " * len(right_lines[0])
            result.append(l + sep + r)
        return result

    def _pad_to_width(self, lines, width):
        return [ln.ljust(width) for ln in lines]

    # ── Render ────────────────────────────────────────────────────────────────

    def render(self):
        if not self.nodes:
            return ""

        result_lines = [""]
        i = 0
        while i < len(self.nodes):
            node = self.nodes[i]
            ntype = node["type"]
            label = node.get("label")

            if ntype == "decision":
                left = self._draw_node(node)
                mid = len(left) // 2
                width = max(len(l) for l in left) + 2

                # Left branch label row
                if label:
                    parts = str(label).split("/")
                    left[mid] = left[mid].rstrip() + " {}:{}".format(parts[0], ARROW_LEFT)
                left = [ln.ljust(width) for ln in left]

                # Right branch node
                i += 1
                if i < len(self.nodes):
                    right = self._draw_node(self.nodes[i])
                    label2 = self.nodes[i].get("label", "")
                    if label2:
                        parts2 = str(label2).split("/")
                        right[mid] = right[mid].rstrip() + " {}:{}".format(parts2[0], ARROW_RIGHT)
                else:
                    right = [" " * width]

                # Arrow line connecting them
                arrow_cell = " {} ".format(self.arrow).center(width)
                if label:
                    arrow_cell = "{}:{}".format(str(label).split("/")[0], ARROW_RIGHT).ljust(width)

                # Insert arrow column between left and right
                result_lines = self._hconcat(result_lines, left)
                arrow_col = [" " * width for _ in result_lines]
                if mid < len(arrow_col):
                    arrow_col[mid] = arrow_cell
                result_lines = self._hconcat(result_lines, arrow_col)
                result_lines = self._hconcat(result_lines, right)
                i += 1
            else:
                node_lines = self._draw_node(node)
                width = max(len(l) for l in node_lines) + 2
                node_lines = [ln.ljust(width) for ln in node_lines]

                if result_lines == [""]:
                    result_lines = node_lines
                else:
                    result_lines = self._hconcat(result_lines, node_lines)

                # Arrow column between nodes
                if i < len(self.nodes) - 1:
                    arrow_col = [" " * width for _ in result_lines]
                    if len(result_lines) // 2 < len(arrow_col):
                        arrow_col[len(result_lines) // 2] = " {} ".format(self.arrow).center(width)
                    result_lines = self._hconcat(result_lines, arrow_col)

            i += 1

        return "\n".join(result_lines)


def flowchart(*steps, **kwargs):
    """Quick helper: build a simple linear flowchart from strings."""
    style = kwargs.get("style", "box")
    arrow = kwargs.get("arrow", ARROW_RIGHT)
    fc = Flowchart(style=style, arrow=arrow)
    for s in steps:
        fc.add(s)
    return fc.render()


__all__ = [
    "Flowchart",
    "flowchart",
    "NODE_CHARS",
    "STYLE_GLYPHS",
    "ARROW_RIGHT",
    "ARROW_LEFT",
    "ARROW_DOWN",
    "ARROW_UP",
    "BRANCH_LABELS",
]