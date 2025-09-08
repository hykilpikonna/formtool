# formtool

Easy ffmpeg shortcuts

- [x] Can batch convert files
- [x] Automatically use best settings
- [x] You can override params
- [x] Deletes original files if you want
- [x] Shortcuts that are actually short
- [x] has rgb :3



https://github.com/user-attachments/assets/82d32a7f-6fa2-4d88-a8c8-35dd9e594287



## Install

```bash
pip install formtool
```

## Usage

```bash
# Compress everything to flac, save space without losing quality
fflac **/*.wav

# If you want to send some music but flac is too big: convert to mp3 v0
fmp3 song.flac

# If you want to archive videos
fav1 *.mp4

# If you want to send videos to telegram
fx264 video.mkv
```

### Overriding default parameters

```bash
# If you want shrink file size even more, for example
fav1 *.mp4 -crf 50
```

### Screenshots

<img width="1913" height="1638" alt="image" src="https://github.com/user-attachments/assets/011e28b0-bb02-43f9-8770-c5160bed80ef" />

<img width="1254" height="837" alt="image" src="https://github.com/user-attachments/assets/8106da81-4415-4459-b9b3-3beffee07f48" />


