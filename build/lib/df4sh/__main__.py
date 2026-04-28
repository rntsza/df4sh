import sys

from df4sh.config import load_app_config


def main() -> None:
    load_app_config()
    sys.exit(0)


if __name__ == "__main__":
    main()
