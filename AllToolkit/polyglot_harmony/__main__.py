"""CLI entry point for Polyglot Harmony."""

from pathlib import Path
from .harmony import analyze_harmony


def main() -> None:
    config_path = str(Path(__file__).parent.parent / "language_rotation.json")
    report = analyze_harmony(config_path, rotate=True)

    print("=" * 60)
    print("  Polyglot Harmony Report")
    print("=" * 60)
    print(f"  Transition:  {report.previous_language} → {report.current_language}")
    print(f"  Overall Score: {report.overall_score:.2f} / 1.00")
    print(f"  Rotated Index: {report.new_index}")
    print("-" * 60)
    print("  Dimensions:")
    for dim in report.dimensions:
        bar = "█" * int(dim.score * 10) + "░" * (10 - int(dim.score * 10))
        print(f"    {dim.label:20s} [{bar}] {dim.score:.2f}")
        print(f"      {dim.description}")
    print("-" * 60)
    print("  Transfer Tips:")
    for tip in report.transfer_tips:
        print(f"    • {tip}")
    print("-" * 60)
    print(f"  {report.synergy_summary}")
    print("=" * 60)


if __name__ == "__main__":
    main()