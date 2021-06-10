#!/usr/bin/env python3
"""UNC to URL Converter."""

from __future__ import print_function
import sys

import argparse
import unicodedata
from urllib.parse import quote, unquote

import argcomplete  # type: ignore

# from . import __version__
__version__ = "0.0.2"  # for Alfred Workflow
sys.path.insert(0, "./lib")  # for Alfred Workflow


def main(args=None):
    """Start point."""
    if args is None:
        main(get_parser().parse_args())
    else:
        if args.reverse:
            print(url_to_unc(args.unc))
        else:
            print(unc_to_url(args.unc, args.file))


def unc_to_url(unc: str, as_file: bool = False):
    """Convert UNC to file or smb URL."""
    unc = unicodedata.normalize("NFC", unc).strip()  # e.g., for the Alfred Workflow
    url = unc.replace("\\\\", "smb://").replace("\\", "/")
    if as_file:  # for Windows 10, but don't encode Umlauts
        url = url.replace("smb://", "file://").replace(" ", "%20")
    else:  # for macOS / Linux
        url = quote(url, safe=":/")
    return url


def url_to_unc(url: str):
    """Convert URL und UNC."""
    url = url.strip()
    url = url.replace("smb://", "\\\\")
    url = url.replace("file://", "\\\\")
    url = url.replace("/", "\\")
    return unquote(url)


def get_parser():
    """Create urn line argument parser."""
    parser = argparse.ArgumentParser(description="Simple UNC to URL tool.")

    parser.add_argument("unc", help="An Uniform Naming Convention (UNC) link")

    parser.add_argument(
        "-r",
        "--reverse",
        dest="reverse",
        help="Reverse the conversation (url2unc)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "-f",
        "--file",
        dest="file",
        help="File URL (file://)",
        action="store_true",
        default=False,
    )

    parser.add_argument(
        "--version",
        "-v",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__),
    )

    argcomplete.autocomplete(parser)

    return parser


if __name__ == "__main__":
    main()
