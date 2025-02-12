"""
    It's been used to check the number of narrations used for each video in the nlq_train and nlq_val files.
    and to calculate for each video how many narrations have been used and the mean duration of each narration.
"""

import json
import ijson
import os


def generate_videos_list(
    filepath="/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/narrations/annotations/ego4d.json",
):
    """
    Generate a list of videos from the ego4d file

    Args:
        filepath (str): path to the ego4d file

    Returns:
        list: list of videos
        
    """
    list_videos = []
    try:
        # Read ego4d file
        with open(filepath, "r") as f:
            data = json.load(f)
            for video in data["videos"]:
                list_videos.append(video)
        return list_videos
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e} - {type(e)}")
        print("Please check the file path and try again.")


def search_video(video_id, list_videos):
    """
    Search for a video in the list of videos

    Args:
        video_id (str): video id to search for

    Returns:
        dict: video information or None if not found
    """
    for video in list_videos:
        if video["video_uid"] == video_id:
            return video
    return None


def calculate_narrations(list_videos, output_file="output/output.json"):
    """
    Calculate for each video how many narrations have been used and the mean duration of each narration
    """
    data_narrations = []
    try:
        for i in range(1, 2):
            print("Analyzing file")
            with open(
                f"/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/narrations/data/{i}.json", "r"
            ) as f:
                for obj in ijson.items(f, "item"):
                    for key, value in obj.items():
                        dict_data = {}
                        if "narration_pass_2" in value:
                            result = search_video(key, list_videos)
                            if result is not None:
                                dict_data["video_id"] = key
                                dict_data["sec"] = result["duration_sec"]
                                dict_data["length_narr"] = len(
                                    value["narration_pass_2"]["narrations"]
                                )
                                dict_data["mean"] = result["duration_sec"] / len(
                                    value["narration_pass_2"]["narrations"]
                                )
                                data_narrations.append(dict_data)
            data_narrations.append(dict_data)

            return data_narrations

        # Check if folder exists
        if not os.path.exists("output"):
            os.makedirs("output")

        # Write data to a new file
        with open(output_file, "w") as f:
            json.dump(data_narrations, f, indent=4)

    # catch errors
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e} - {type(e)}")
        print("File", i, "could not be read.")
        print("Please check the file path and try again.")


def count_narrations(
    path_train="/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/narrations/annotations/v1/annotations/nlq_train.json",
    path_val="/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/narrations/annotations/v1/annotations/nlq_val.json",
):
    """
    Count how many narrations have been used for each video in nlq_train and nlq_val
    """
    list_data = []
    total = 0
    try:
        with open(path_train, "r") as f:
            data = json.load(f)
            for video in data["videos"]:
                count = 0
                for clip in video["clips"]:
                    for anno in clip["annotations"]:
                        count += len(anno["language_queries"])
                list_data.append(
                    {"video_uid": video["video_uid"], "len_narrations": count}
                )
                total += count

        print("Total narrations in nlq_train:", total)
        print("Total videos in nlq_train:", len(list_data))

        with open(path_val, "r") as f:
            data = json.load(f)
            for video in data["videos"]:
                count = 0
                for clip in video["clips"]:
                    for anno in clip["annotations"]:
                        count += len(anno["language_queries"])
                # Check if video is already in list_data
                found = False
                for item in list_data:
                    if item["video_uid"] == video["video_uid"]:
                        found = True
                        break
                if not found:
                    list_data.append(
                        {
                            "video_uid": video["video_uid"],
                            "len_narrations_val": count,
                            "found": False,
                        }
                    )
                else:
                    for item in list_data:
                        if item["video_uid"] == video["video_uid"]:
                            item["len_narrations_val"] = count
                            break

        # Write data to a new file
        with open("output/output_training.json", "w") as f:
            json.dump(list_data, f, indent=4)

        return list_data
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"An error occurred: {e} - {type(e)}")


def combine_data(data_narrations, list_data):
    """
    Combine the information from the two files
    """
    data_combined = []
    total = 0
    for info in data_narrations:
        for item in list_data:
            if info["video_id"] == item["video_uid"]:
                data_combined.append(
                    {
                        "video_id": info["video_id"],
                        "sec": info["sec"],
                        "length_narr": info["length_narr"],
                        "mean": info["mean"],
                        "len_narrations": (
                            item["len_narrations"] if "len_narrations" in item else 0
                        ),
                        "len_narrations_val": (
                            item["len_narrations_val"]
                            if "len_narrations_val" in item
                            else 0
                        ),
                    }
                )
                break

    # Write data to a new file
    with open("output/output_combined.json", "w") as f:
        json.dump(data_combined, f, indent=4)


if __name__ == "__main__":
    list_videos = generate_videos_list()
    data_narrations = calculate_narrations(list_videos)
    list_data = count_narrations()
    combine_data(data_narrations, list_data)
