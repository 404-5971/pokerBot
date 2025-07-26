import subprocess


def main() -> None:
    commands: list[list[str]] = [
        ["uv", "run", "black", "src/"],
        ["uv", "run", "isort", "src/"],
        ["uv", "run", "mypy", "src/"],
        ["uv", "run", "src/main.py"],
    ]

    for command in commands:
        result: subprocess.CompletedProcess[bytes] = subprocess.run(command)
        if result.returncode != 0:
            print(
                f"Command {' '.join(command)} failed with exit code {result.returncode}"
            )
            break


if __name__ == "__main__":
    main()
