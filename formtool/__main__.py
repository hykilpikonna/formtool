from subprocess import check_call
from pathlib import Path
import argparse
import sys


def main():
    agupa = argparse.ArgumentParser("formtool", "ffmpeg shortcuts")
    agupa.add_argument('files', nargs='+', help="One or more video files to compress.")
    agupa.add_argument('--keep', action='store_true', help="Keep original files after compression.")
    args, passthrough = agupa.parse_known_args()

    # Process each file provided on the command line
    for inf in args.files:
        inf = Path(inf)

        if not inf.exists():
            print(f"Error: File not found, skipping: {inf}", file=sys.stderr)
            continue

        ouf = f'{inf.stem}.comp.av1.mp4'
        print(f"-> Compressing '{inf.name}'...")

        try:
            params = {
                '-c:v': 'libsvtav1',
                '-crf': '36',
                '-preset': '8',
                '-c:a': 'libopus',
                '-b:a': '96k',
                '-vbr': 'on',
            }
            # Check for any passthrough arguments and add them to params (overrides defaults)
            _tmp = iter(passthrough)
            for k, v in zip(_tmp, _tmp):
                print(f"   Overriding parameter: {k} {v} (was {params.get(k, 'not set')})")
                params[k] = v

            # Construct and run the ffmpeg command
            cmd = ['ffmpeg', '-hide_banner', '-i', inf.absolute(), *sum(([k, v] for k, v in params.items()), []), ouf]
            print(f"   Running command: {' '.join(cmd)}")

            check_call(cmd)
            print(f"   Compression successful.")

            if not args.keep:
                inf.unlink()
                print(f"   Removed original file: '{inf.name}'")

            print()

        except Exception as e:
            print(f"An error occurred while processing {inf.name}: {e}", file=sys.stderr)
            print("   Leaving original file intact.\n", file=sys.stderr)


if __name__ == "__main__":
    main()
