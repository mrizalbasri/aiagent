from functions.get_files_info import get_files_info


def main() -> None:
    for directory, label in (
        (".", "current directory"),
        ("pkg", "'pkg' directory"),
        ("/bin", "'/bin' directory"),
        ("../", "'../' directory"),
    ):
        print(f"Result for {label}:")
        result = get_files_info("calculator", directory)
        for line in result.splitlines():
            print(f"  {line}")
        print()


if __name__ == "__main__":
    main()
