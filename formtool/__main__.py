from subprocess import check_call
from pathlib import Path
import argparse
import sys

from hypy_utils import printc


def main():
    agupa = argparse.ArgumentParser("formtool", "ffmpeg shortcuts")
    agupa.add_argument('files', nargs='+', help="One or more video files to compress.")
    agupa.add_argument('--keep', action='store_true', help="Keep original files after compression.")
    args, passthrough = agupa.parse_known_args()

    # Process each file provided on the command line
    for inf in args.files:
        inf: Path = Path(inf)

        if not inf.exists():
            printc(f"&cError: File not found, skipping: {inf}")
            continue

        ouf = inf.with_name(f'{inf.stem}.comp.av1.mp4')
        printc(f"&e-> Compressing '{inf.name}' > '{ouf.name}'")

        try:
            params = {
                '-c:v': 'libsvtav1',
                '-crf': '36',
                '-preset': '8',
                '-c:a': 'libopus',
                '-b:a': '96k',
                '-vbr': 'on',
            }
            old_size = inf.stat().st_size

            # Check for any passthrough arguments and add them to params (overrides defaults)
            _tmp = iter(passthrough)
            for k, v in zip(_tmp, _tmp):
                printc(f"&a   Overriding parameter: {k} {v} (was {params.get(k, 'not set')})")
                params[k] = v

            # Construct and run the ffmpeg command
            cmd = ['ffmpeg', '-hide_banner', '-i', inf.absolute(), *sum(([k, v] for k, v in params.items()), []), ouf]
            printc(f"&e   Running command: {' '.join(cmd)}")

            check_call(cmd)
            printc(f"&a   Compression successful :)")
            new_size = ouf.stat().st_size
            ratio = new_size / old_size
            printc(f"&a   Size: {old_size / 1_000_000:.2f} MB -> {new_size / 1_000_000:.2f} MB ({ratio:.2%})")

            if not args.keep:
                if new_size >= old_size:
                    printc(f"&c   Warning: Compressed file is not smaller than original! Keeping original file.")
                else:
                    inf.unlink()
                    printc(f"&c   Removed original file: '{inf.name}'")

            print()

        except Exception as e:
            printc(f"&cAn error occurred while processing {inf.name}: {e}")
            printc("&c   Leaving original file intact.\n")


if __name__ == "__main__":
    main()
