from functions.run_python_file import run_python_file


def main() -> None:
    for file_path, args in (
        ("main.py", None),
        ("main.py", ["3 + 5"]),
        ("tests.py", None),
        ("../main.py", None),
        ("nonexistent.py", None),
        ("lorem.txt", None),
    ):
        print(f"Result for {file_path}, args={args}:")
        print(run_python_file("calculator", file_path, args))
        print()


if __name__ == "__main__":
    main()
