import pyperclip

def convert_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Replace line breaks with \n
        content = content.replace('\n', '\\n').replace('"', '\\"')

        # Copy to clipboard
        pyperclip.copy(content)
        print("Content copied to clipboard with line breaks replaced.")
    
    except IOError:
        print("An error occurred while reading the file.")

# Replace with the path to your Markdown file
file_path = 'prompt.md'
convert_markdown(file_path)