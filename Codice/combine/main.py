import json

def combine_json_files(file1, file2):
    with open(file1, "r") as f1, open(file2, "r") as f2:
        data1 = json.load(f1)
        data2 = json.load(f2)

    for video2, video1 in zip(data2["videos"], data1["videos"]):
        for clip2, clip1 in zip(video2["clips"], video1["clips"]):
                for queries2, queries1 in zip(clip2["annotations"], clip1["annotations"]):
                    for lq2, lq1 in zip(queries2["language_queries"], queries1["language_queries"]):
                        if "query" not in lq2 and "query" in lq1:
                            #Get query from data1
                            pattern = "These narrations"
                            if pattern in lq1["query"]:
                                lq2["query"] = ""
                            else:
                                lq2["query"] = lq1["query"]    
                        else:
                            pass

    return data2                    

if __name__ == "__main__":
    file1 = "/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/combine/data/annotations_train_0_150.json"
    file2 = "/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/combine/data/annotations_train_158_1344.json"
    output_file = "/Users/andreaongaro/Documents/Magistrale/Torino/Corsi/2_ANNO/AdvanceMachineLearning/Progetto/Code/combine/output/annotations_train_0_158.json"

    data = combine_json_files(file1, file2)

    with open(output_file, "w") as file:
        json.dump(data, file, indent=4)
    print("Files combined successfully.")
