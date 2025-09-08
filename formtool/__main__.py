from subprocess import check_call
from pathlib import Path
import argparse
import sys


def main():
    agupa = argparse.ArgumentParser("formtool", "ffmpeg shortcuts")
    arg = agupa.add_argument

    arg('files', nargs='+', help="One or more video files to compress.")
    arg('--crf', type=int, default=36, help="Constant Rate Factor for quality control (lower is better quality)")
    arg('--preset', type=int, default=8, help="Encoding preset for speed/quality trade-off.")

    args = agupa.parse_args()

    # Process each file provided on the command line
    for file_str in args.files:
        video_path = Path(file_str)

        if not video_path.exists():
            print(f"Error: File not found, skipping: {video_path}", file=sys.stderr)
            continue

        output_filename = f'{video_path.stem}.comp.av1-crf{args.crf}.mp4'
        print(f"-> Compressing '{video_path.name}'...")
        print(f"   CRF: {args.crf}, Preset: {args.preset}, Output: '{output_filename}'")

        try:
            # Construct and run the ffmpeg command
            check_call([
                'ffmpeg',
                '-hide_banner', '-i', video_path,
                '-c:v', 'libsvtav1',
                '-crf', str(args.crf),
                '-preset', str(args.preset),
                '-c:a', 'libopus',
                '-b:a', '96k', '-vbr', 'on',
                output_filename
            ])

            print(f"   Compression successful.")

            # Remove the original video after successful compression
            video_path.unlink()
            print(f"   Removed original file: '{video_path.name}'\n")

        except Exception as e:
            print(f"An error occurred while processing {video_path.name}: {e}", file=sys.stderr)
            print("   Leaving original file intact.\n", file=sys.stderr)


if __name__ == "__main__":
    main()
