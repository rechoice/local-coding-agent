from functions.get_file_content import get_file_content

def main():
    content = get_file_content("calculator", "lorem.txt")
    print(len(content))  
    print(content[-200:])  

    print(get_file_content("calculator", "main.py"))
    print(get_file_content("calculator", "pkg/calculator.py"))
    print(get_file_content("calculator", "/bin/cat"))
    print(get_file_content("calculator", "pkg/does_not_exist.py"))

if __name__ == "__main__":
    main()