"""Configure local simulation includes for an existing SCL08 PDK."""
from argparse import ArgumentParser
from pathlib import Path


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("models", type=Path, help="Path to SCL08 ngspice_models49")
    pdk = parser.parse_args().models.expanduser().resolve()
    for relative in ("mos/tntp49_5v", "res/typ/ppr"):
        if not (pdk / relative).is_file():
            parser.error(f"Missing SCL08 model file: {pdk / relative}")
    root = Path(__file__).resolve().parent
    for name in ("bench_support.spice", "bench_support_schematic.spice"):
        source = (root / (name + ".in")).read_text()
        (root / name).write_text(source.replace("@SCL08_MODELS@", str(pdk)))
        print(f"Configured {name}")


if __name__ == "__main__":
    main()
