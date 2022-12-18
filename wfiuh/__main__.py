import click

from .curve_fitting.__main__ import command as curve_fitting
from .param_distribution.__main__ import main as param_distribution


@click.group(name="wfiuh", context_settings={"show_default": True})
def main() -> None:
    pass


main.add_command(cmd=curve_fitting, name="curve-fitting")
main.add_command(cmd=param_distribution, name="param-dis")


if __name__ == "__main__":
    main()
