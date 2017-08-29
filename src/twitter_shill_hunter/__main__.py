import argparse
from gen_logo import Logo


def main():
    """
    Function to kick off the show.
    """

    logo = Logo()
    logo.generate_logo()
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "username",
        help="a twitter username")
    parser.add_argument(
        "dialect",
        help=" supposed English dialect of target")
    args = parser.parse_args()
    process_input(args.username, args.dialect)


def process_input(username, dialect):
    """
    Generate the object
    to start hunting
    for dialect changes 
    by twitter username
    """

    print "testing"


if __name__ == "__main__":
    main()
