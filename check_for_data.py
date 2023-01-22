import json
import find_file_path
import os
import datetime

today = str(datetime.date.today())

def main(category):
    file_path = find_file_path.main(category)
    category = category.replace(" ", "_")
    with open(file_path + "data.json") as f:
        data = json.load(f)
    if len(data["articles"]) == 0:
        return False
    else:
        with open(file_path + "old_data.json", "w") as f:
            json.dump(data,f)
        print("Old data discovered and saved.")
        os.remove(file_path + "data.json")
        with open("data_template.json", "r") as f:
            text = f.read()
            with open(file_path + "data.json", "w") as f:
                f.write(text)

