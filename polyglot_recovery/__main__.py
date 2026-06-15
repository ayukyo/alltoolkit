"""CLI entry point for polyglot_recovery."""

from polyglot_recovery.src.recovery import generate_recovery_report, format_recovery_report, run_tests
import sys


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        report = generate_recovery_report()
        print(format_recovery_report(report))


if __name__ == "__main__":
    main()