"""Entry point for `python -m pulse`."""

from pulse.app import PulseApp


def main() -> None:
    app = PulseApp()
    app.run()


if __name__ == "__main__":
    main()
