# UltraVision-YOLO

A simple terminal tool for object detection with [Ultralytics YOLO](https://github.com/ultralytics/ultralytics).
It gives you a clean menu to run detection on a single image, a whole folder of images, or a video.

## Features

- Menu-based: Single Image, Batch Folder, Single Video
- Downloads the model (`yolo26x.pt`) automatically if it is not found
- Runs offline after the model is downloaded
- Progress bar for batch processing and model download
- Clean exit with Ctrl+C, and errors do not crash the menu
- Tested on Termux (Android). Windows and macOS have not been tested.

## Requirements

- Python 3.8 or newer
- `ultralytics` and `rich`

```bash
pip install -r requirements.txt
```

## Usage

```bash
python ultravision.py
```

Choose an option from the menu:

| Option | Task                       |
|--------|----------------------------|
| 1      | Single Image               |
| 2      | Batch Folder (Manual Path) |
| 3      | Single Video               |
| exit   | Close Script               |

## Where are the files?

Run the script from the folder where you want everything to stay.
The model file and the `runs/` results folder are created in the **current folder**
(the folder you run the command from).

```
.
├── ultravision.py
├── yolo26x.pt          <- model (downloaded on first run)
└── runs/
    └── detect/
        ├── predict/
        └── predict2/   <- results of each run
```

## Note

An internet connection is required on the first run to download the model file.
After that, the script works offline.

`yolo26x.pt` is the largest YOLO26 model. On a phone or a PC without a GPU it can be slow
and needs a lot of RAM.

## License

This project is licensed under the **GNU Affero General Public License v3.0 (AGPL-3.0)**.
See the [LICENSE](LICENSE) file for details.

## Credits

This project uses the following open-source tools:

- [Ultralytics YOLO](https://github.com/ultralytics/ultralytics) (AGPL-3.0) for object detection.
  The model weights (`yolo26x.pt`) are downloaded from the official
  [Ultralytics assets releases](https://github.com/ultralytics/assets/releases)
  and are not included in this repository.
- [Rich](https://github.com/Textualize/rich) (MIT) for the terminal menu and progress bars.

Made by Hansraj