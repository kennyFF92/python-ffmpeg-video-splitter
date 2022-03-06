import os
import json
import argparse
import subprocess


def _parse_args():
    parser = argparse.ArgumentParser(
        usage="python3 split_video_folder.py -i ... -s split_info.json"
    )
    parser.add_argument(
        "-i", "--input_dir", required=True, help="Directory with videos"
    )
    parser.add_argument(
        "-s", "--split_file", required=True, help="JSON file with split info"
    )
    args, _ = parser.parse_known_args()

    return args


def get_video_length(video_name):
    length_cmd = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        video_name,
    ]
    length = subprocess.check_output(length_cmd).strip()

    return int(float(length))


if __name__ == "__main__":
    args = _parse_args()
    assert (
        os.path.splitext(args.split_file)[1] == ".json"
    ), "Split info must be in a JSON file"

    with open(args.split_file, "r") as fp:
        split_info = json.load(fp)

    for video_info in split_info:
        video_path = os.path.join(args.input_dir, video_info["name"])
        split_cmd = [
            "ffmpeg",
            "-i",
            video_path,
            "-vcodec",
            "copy",
            "-acodec",
            "copy",
            "-y",
        ]
        video_name, video_ext = os.path.splitext(video_path)

        for split_count, (split_start, split_end) in enumerate(
            video_info["split_time"]
        ):
            split_name = os.path.join(
                args.input_dir,
                video_name + "_" + str(split_count) + "." + video_ext,
            )
            print(split_name)

            split_args = [
                "-ss",
                str(split_start),
                "-t",
                str(split_end - split_start),
                split_name,
            ]
            print(split_cmd + split_args)
            subprocess.check_output(split_cmd + split_args)

            split_count += 1
