# latex_elaboration_improver

This is a simple tool to improve the elaboration of latex files.

## How to use it
Pass either the path to a file or a directory as an argument to the script.
You can also pass the language as a second argument, the default is `German`.

'''bash
python3 main.py [/path/to/file/or/directory] [language]
'''


It will create a new folder called `x_improved` in the same directory as the file or directory you passed as an argument.

## What it does
It will go through all the files in the directory you passed as an argument and will:
- Each sentence will be on a new line
- It will split the sentences to segments by sections, subsections, subsubsections, paragraphs or lines
- Then it will call gpt to improve the elaboration of each segment
- Finally it will merge the segments back together and write them to the new file

# Requirements
- Installed requirements from `requirements.txt`
- OpenAI API key set as an environment variable called `OPENAI_API_KEY_LATEX`
