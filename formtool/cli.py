import argparse

from . import defaults, main


def cli(fmt: str | None = None):
    agupa = argparse.ArgumentParser("formtool", "ffmpeg shortcuts")
    if fmt is None:
        agupa.add_argument('format', choices=defaults.keys(), help="Compression format to use.")
    agupa.add_argument('files', nargs='+', help="One or more files to compress.")
    agupa.add_argument('--keep', action='store_true', help="Keep original files after compression.")
    args, passthrough = agupa.parse_known_args()

    main(fmt or args.format, args.files, args.keep, passthrough)


def av1():
    cli('av1')


def x264():
    cli('x264')


def mp3():
    cli('mp3')


def opus():
    cli('opus')


def flac():
    cli('flac')
