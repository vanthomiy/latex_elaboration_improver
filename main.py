import os
import sys

import gpt


def recursive_split(text: str, max_allowed_token: int, level: int) -> list[str]:
    splitters = ["\\section", "\\subsection", "\\subsubsection", "\n\n", "\n"]
    if level >= len(splitters):
        return [text]
    result = []
    segments = text.split(splitters[level])
    # add the splitters back at the beginning
    for i in range(1, len(segments)):
        segments[i] = splitters[level] + segments[i]

    # check if max token limit is exceeded
    for segment in segments:
        if gpt.count_token(segment) > max_allowed_token:
            result.extend(recursive_split(segment, max_allowed_token, level + 1))
        else:
            result.append(segment)

    return result


def handle_file(file_path: str) -> None:
    """
    Handle a latex file.
    We will do the following:
    1. Read the latex file.
    2. Apply basic formatting.
    3. Split the file into sections, subsections, etc.
    4. Improve text for each Segment with GPT-4.
    5. Write the output to a file.

    :param file_path: The path to the latex file.
    """

    max_allowed_token = 2048

    # create a new folder for the output on the same level as the input folder
    # get the path to the folder
    folder_path = os.path.dirname(file_path)
    # create a new folder
    output_folder_path = folder_path + "_improved"
    if not os.path.exists(output_folder_path):
        os.mkdir(output_folder_path)
    # new file path
    improved_file_path = os.path.join(output_folder_path, os.path.basename(file_path))
    # read the output to latex as utf-8 so that we can handle special characters
    with open(file_path, "r", encoding="utf-8") as f:
        latex = f.read()

    # region 2. apply basic formatting
    # Add a new line after each sentence
    latex = latex.replace(". ", ".\n")
    # endregion 2. apply basic formatting

    # region 3. split the file into sections, subsections, etc.

    # split and get list
    segments = recursive_split(latex, max_allowed_token, 0)
    print(len(segments))

    # endregion 3. split the file into sections, subsections, etc.

    # region 4. improve text for each Segment with GPT-4
    for i in range(len(segments)):
        print("Segment {} of {}".format(i + 1, len(segments)))
        segments[i] = gpt.call(segments[i], "German")
    latex = "".join(segments)

    # endregion 4. improve text for each Segment with GPT-4

    # region 5. write the output to a file

    # write the output to a new file with utf-8 encoding
    with open(improved_file_path, "w", encoding="utf-8") as f:
        f.write(latex)

    # endregion 5. write the output to a file


if __name__ == "__main__":
    # check if the user has provided a path
    if len(sys.argv) < 2:
        path = input("Please provide a path to the latex content:\n")
    else:
        path = sys.argv[1]

    # check if the folder exists
    if not os.path.exists(path):
        print("The path does not exist.")
        sys.exit(1)

    # check if the path is a folder or a file
    if os.path.isfile(path):
        print("The path is a file.")
        handle_file(path)
        sys.exit(0)

    print("The path exists.")
    # list all latex files in the folder
    latex_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(".tex"):
                latex_files.append(os.path.join(root, file))

    # check if there are any latex files
    if len(latex_files) == 0:
        print("There are no latex files in the folder.")
        sys.exit(1)

    # print the count of latex files
    print("There are {} latex files in the folder.".format(len(latex_files)))
    for file in latex_files:
        print(file)
        # ask the user if they want to process the file
        # if yes, process the file
        if input("Do you want to process this file? (y/n): ") == "y":
            handle_file(file)
