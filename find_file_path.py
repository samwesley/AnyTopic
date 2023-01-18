import variables
import datetime

#Usage: copy the following line
# file_path = find_file_path.main(category)
today = str(datetime.date.today())

folderName = str(today)



def main(category):
    path = "categories/" + variables.categories[category] + "/" + folderName + "/final/"

    return path