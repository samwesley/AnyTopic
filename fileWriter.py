

def writeTextToFile(filePath, fileTitle, fileContent):
    fileTitle = str(fileTitle)
    with open(filePath + fileTitle + ".txt", "w") as f:
        f.write(fileContent)


    print("File saved as " + filePath + fileTitle + ".txt")


def appendTextToFile(filePath, fileTitle, fileContent):
    fileTitle = str(fileTitle)
    with open(filePath + fileTitle + ".txt", "a") as f:
        f.write(fileContent)

    print("File appended to " + filePath + fileTitle + ".txt")
