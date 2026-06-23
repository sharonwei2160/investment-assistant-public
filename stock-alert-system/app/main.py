import sys

from workflow import run_with_error_handling


def main():
    target_market = sys.argv[1] if len(sys.argv) > 1 else None
    run_with_error_handling(target_market)


if __name__ == "__main__":
    main()