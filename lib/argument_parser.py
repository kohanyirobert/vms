import argparse
from .yaml_parser import yaml


def get_args():
    # First pass, unknown variants are ignored
    parser = _create_base_parser(True)
    known_args, remaining_args = parser.parse_known_args()
    _normalize_args(known_args)
    if known_args.debug:
        print(known_args, remaining_args)
    # For the second pass a stricter parser is used
    # and additional arguments are added dynamically
    parser = _create_base_parser(False, known_args.variants)
    args = parser.parse_args()
    _normalize_args(args)
    if args.debug:
        print(args)
    return args


def _create_base_parser(first_run, known_variants=[]):
    all_variants = ["base", "nossh", "mininet", "desktop", "db", "www"]
    seen_variants = []

    def existing_variant_type(x):
        return x if x in all_variants else None

    def seen_variant_type(x):
        if x in seen_variants:
            raise argparse.ArgumentTypeError(f"invalid choice: '{x}' already choosen")
        seen_variants.append(x)
        if not x in all_variants:
            choices = ", ".join(map(lambda x: "'" + x + "'", all_variants))
            raise argparse.ArgumentTypeError(
                f"invalid choice: '{x}' (choose from {choices})"
            )
        return x

    def yaml_string(x):
        try:
            return yaml.load(x)
        except:
            raise argparse.ArgumentTypeError(f"invalid YAML string: {x}")

    def yaml_file(x):
        try:
            with open(x) as f:
                yaml.load(f)
            return x
        except:
            raise argparse.ArgumentTypeError(f"invalid YAML file: {x}")

    parser = argparse.ArgumentParser()
    parser.add_argument("--template", choices=["ubuntu"], default="ubuntu")
    parser.add_argument("--release", choices=["18.04", "20.04"], default="18.04")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--keep-base-registered", action="store_true")
    parser.add_argument(
        "variants",
        metavar="variant",
        type=existing_variant_type if first_run else seen_variant_type,
        nargs="*",
        default=all_variants,
    )
    for variant in known_variants:
        parser.add_argument(
            f"--extra-{variant}-config", type=yaml_string, action="append"
        )
        parser.add_argument(f"--extras-{variant}-config-file", type=yaml_file)
    return parser


def _normalize_args(args):
    # During the first pass invalid variants are ignored and represented with `None`
    # in the available list of variants, filtering them out for good measure
    args.variants = [x for x in args.variants if not x == None]

    # The `base` variant must always be the first thing to be built when present
    if "base" in args.variants:
        args.variants.pop(args.variants.index("base"))
        args.variants.insert(0, "base")