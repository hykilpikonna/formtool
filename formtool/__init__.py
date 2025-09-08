import argparse
import glob
from pathlib import Path
from subprocess import check_call

from hypy_utils import printc


defaults = {
    'av1': {
        '-c:v': 'libsvtav1',
        '-crf': '36',
        '-preset': '8',
        '-c:a': 'libopus',
        '-b:a': '96k',
        '-vbr': 'on',
    },
    'x264': {  # For older devices
        '-c:v': 'libx264',
        '-crf': '23',
        '-preset': 'medium',
        '-c:a': 'aac',
        '-b:a': '128k',
    },
    'mp3v0': {  # V0
        '-c:a': 'libmp3lame',
        '-q:a': '0',
    },
    'opus': {
        '-c:a': 'libopus',
        '-b:a': '192k',
        '-vbr': 'on',
    },
    'flac': {
        '-c:a': 'flac',
        '-compression_level': '7',
    },
}
suffixes = {
    'av1': '.av1-{-crf}.mp4',
    'x264': '.x264-{-crf}.mp4',
    'mp3v0': '.v{-q:a}.mp3',
    'opus': '.v{-b:a}.opus',
    'flac': '.flac',
}


def main(fmt: str, files: list[str], keep: bool, passthrough: list[str]):
    # Process each file provided on the command line
    files = [
        Path(p)
        for pattern in files
        for p in glob.glob(str(Path(pattern).expanduser()))
        if Path(p).is_file()
    ]
    printc(f"&e> Using format: {fmt}")
    printc(f"&e> Found {len(files)} files to process.")
    printc(f"&e> Keep original files: {'Yes' if keep else 'No'}")
    printc(f"&e> Passthrough parameters: {passthrough if passthrough else 'None'}")
    print()
    for inf in files:
        printc("&e-----------------------------------------")
        try:
            params = defaults[fmt].copy()
            old_size = inf.stat().st_size

            # Check for any passthrough arguments and add them to params (overrides defaults)
            _tmp = iter(passthrough)
            for k, v in zip(_tmp, _tmp):
                printc(f"&a> Overriding parameter: {k} {v} (was {params.get(k, 'not set')})")
                params[k] = v

            end = suffixes[fmt].format(**params)
            if inf.name.endswith(end):
                printc(f"&c> Error: File already has target suffix '{end}', skipping: {inf.name}")
                continue
            ouf = inf.with_name(f'{inf.stem}{end}')
            printc(f"&e+ Compressing '{inf.name}' > '{ouf.name}'")

            # Construct and run the ffmpeg command
            cmd = ['ffmpeg', '-hide_banner', '-i',
                   str(inf),
                   *sum(([k, v] for k, v in params.items()), []),
                   str(ouf)]
            printc(f"&e> Running command: {' '.join(cmd)}")

            check_call(cmd)
            printc(f"&a> Compression successful :)")
            new_size = ouf.stat().st_size
            ratio = new_size / old_size
            printc(f"&a> Size: {old_size / 1_000_000:.2f} MB -> {new_size / 1_000_000:.2f} MB ({ratio:.2%})")

            if not keep:
                if new_size >= old_size:
                    printc(f"&c! Warning: Compressed file is not smaller than original. Keeping original file :(")
                else:
                    inf.unlink()
                    printc(f"&e- Removed original file: '{inf.name}'")

            print()

        except Exception as e:
            printc(f"&c! An error occurred while processing {inf.name}: {e}")
            printc("&c! Leaving original file intact.\n")
