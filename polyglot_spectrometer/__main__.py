"""Entry point for polyglot_spectrometer."""
from src import spectrometer, format_spectrometer, run_tests
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_tests()
    else:
        result = spectrometer()
        print(format_spectrometer(result))
