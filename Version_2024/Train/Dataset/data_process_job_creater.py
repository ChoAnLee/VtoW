import json


if __name__ == "__main__":
    PLAIN_TEXT_DATASET_PATH = ".\\Plain_Text_Datasets\\"
    KEY_STROKE_DATASET_PATH = ".\\Key_Stroke_Datasets\\"
    FILE_NAME = "data_process_job.json"

    job_list = []

    # Create Cleaned Dataset from existing plain text dataset
    mode = "clean"
    src_files = ["Chinese_news.txt", "Chinese_WebCrawlData_cc100.txt", "Chinese_gossip.txt"]
    languages = ["chinese"]


    for src_file in src_files:
        for language in languages:
            dataset_name = None
            if src_file.find("cc100") > 0:
                dataset_name = "cc100"
            elif src_file.find("news") > 0:
                dataset_name = "news"
            elif src_file.find("gossip") > 0:
                dataset_name = "gossip"
            else:
                raise ValueError("Invalid file name: " + src_file)

            job_list.append({
                "mode": mode,
                "description": f"Clean {src_file} to {language}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": PLAIN_TEXT_DATASET_PATH + f"{src_file.replace('.txt', '-ch.txt')}",
                "language": language
                })


    # Create KeyStroke Dataset from existing plain text dataset
    mode = "convert"
    src_files = ["Chinese_news-ch.txt", "Chinese_WebCrawlData_cc100-ch.txt"]
    convert_types = ["bopomofo", "cangjie", "pinyin"]

    for src_file in src_files:
        for convert_type in convert_types:
            dataset_name = None
            if src_file.find("cc100") > 0:
                dataset_name = "cc100"
            elif src_file.find("news") > 0:
                dataset_name = "news"
            else:
                raise ValueError("Invalid file name: " + src_file)

            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + f"{convert_type}-{dataset_name}-0.txt",
                "convert_type": convert_type
                })

    mode = "convert"
    src_files = ["English.txt"]
    convert_types = ["english"]
    for src_file in src_files:
        for convert_type in convert_types:
            job_list.append({
                "mode": mode,
                "description": f"Convert {src_file} to {convert_type}",
                "input_file_path": PLAIN_TEXT_DATASET_PATH + src_file, 
                "output_file_path": KEY_STROKE_DATASET_PATH + f"{convert_type}-0.txt",
                "convert_type": convert_type
                })


    # Create Error Dataset from existing keystroke dataset
    mode = "gen_error"
    src_files = ["bopomofo-news-0.txt", "bopomofo-cc100-0.txt", 
                 "cangjie-news-0.txt", "cangjie-cc100-0.txt", 
                 "pinyin-news-0.txt", "pinyin-cc100-0.txt", 
                 "english-0.txt"]
    error_rates = [0, 0.001, 0.003, 0.01, 0.05, 0.1]
    error_types = ["random"]

    # job_list = []
    for src_file in src_files:
        for error_type in error_types:
            for error_rate in error_rates:
                dataset_name = "-".join(src_file.split("-")[:-1])
                error_rate_name = str(error_rate).replace(".", "_")
                job_list.append({
                    "mode": mode,
                    "description": f"Generate {error_type} error for {dataset_name} with error {error_rate}",
                    "input_file_path": KEY_STROKE_DATASET_PATH + src_file, 
                    "output_file_path": KEY_STROKE_DATASET_PATH + src_file.replace("-0.txt", f"-{error_rate_name}.txt"),
                    "error_type": error_type,
                    "error_rate": error_rate
                    })
                


    with open(FILE_NAME, "w") as f:
        json.dump(job_list, f, indent=4)