import json

def read_file(file1):
    with open(file1, "r") as f1:
        return json.load(f1)

def check_queries(query):
    """
        Check if the query is valid.

        Args:
            query (str): The query to check.
        
        Returns:
            bool: True if the query is valid, False otherwise
    """
    possible_starting_words = ["What", "Who", "Where", "When", "Why", "How", "Which", "Whose", "Whom"]
    for word in possible_starting_words:
        if query.startswith(word):
            return True
    return False
 
def erroneous_queries(data):
    for video in data["videos"]:
        for clip in video["clips"]:
            for queries in clip["annotations"]:
                for lq in queries["language_queries"]:
                    if "query" in lq:
                        if not check_queries(lq["query"]):
                            lq["query"] = ""
    return data

def get_only_correct_values(file1):
    """
        Clean file that has not valid queries.
    
        Args:
            file1 (str): Path to the file to clean.
        
        Returns:
            dict: The cleaned data.
    """
    count = 0
    for video in data["videos"]:
        for clip in video["clips"]:
            for queries in clip["annotations"]:
                queries["language_queries"] = [
                    lq
                    for lq in queries["language_queries"]
                    if "query" in lq and lq["query"] != ""
                ]
                count += len(queries["language_queries"])
    
    for video in data["videos"]:
        for clip in video["clips"]:
            # Filter out annotations where 'language_queries' is empty
            clip["annotations"] = [
                annotation for annotation in clip["annotations"] if annotation["language_queries"]
            ]

    for video in data["videos"]:
        # Filter out clips where 'annotations' is empty or becomes empty after filtering
        video["clips"] = [
            clip for clip in video["clips"] if clip["annotations"]
        ]

    # Filter out videos where the 'clips' list is empty
    data["videos"] = [
        video for video in data["videos"] if video["clips"]
    ]
    print(f"Correct queries: {count}")

    return data

def remove_narrations(data):
    """
        Clean file that has not valid queries.
    
        Args:
            file1 (str): Path to the file to clean.
        
        Returns:
            dict: The cleaned data.
    """

    for video in data["videos"]:
        for clip in video["clips"]:
            for queries in clip["annotations"]:
                for lq in queries["language_queries"]:
                    lq.pop("narrations", None)
    return data

if __name__ == "__main__":
    try: 
        file1 = "/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/combine/output/annotations_val_71_252.json"
        output_file = "/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/clean/output/annotations_val.json"

        data = read_file(file1)

        data = erroneous_queries(data)

        data = get_only_correct_values(data)

        data = remove_narrations(data)

        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)
        print("Files combined successfully.")

    except Exception as e:
        print(f"An error occurred: {e}")
        
