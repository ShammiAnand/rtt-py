import os


class DirWalker:
    """walks the directory and stores all the file contents into a single file"""

    def __init__(self, path: str):
        self.path = DirWalker.__validate_path(path)
        self.files = []
        self.file_contents = {}

    @staticmethod
    def __validate_path(path: str) -> str:
        """validates the path to ensure it is a directory"""

        if not os.path.isdir(path):
            raise ValueError(f"{path} is not a valid directory")

        return path

    def convert(
        self, want_content: bool = False, default_ext: str = ".md"
    ) -> tuple[str, str | None]:
        """
        walks the directory and stores all the file contents into a single file
        and returns the path to the file
        """

        for root, _, files in os.walk(self.path):
            for file in files:
                if file.startswith("."):
                    continue

                if file.endswith(
                    (
                        ".pyc",
                        ".exe",
                    )
                ):
                    continue

                with open(os.path.join(root, file), "r") as f:
                    self.file_contents[file] = f.read()
                    self.files.append(file)

        with open(os.path.join(self.path, f"rtt{default_ext}"), "w") as f:
            for file in self.files:
                f.write(f"# {file}\n")
                f.write("```\n")
                f.write(self.file_contents[file])
                f.write("\n```")
                f.write("\n\n")

        if want_content:
            with open(os.path.join(self.path, f"rtt{default_ext}"), "r") as f:
                content = f.read()

            os.remove(os.path.join(self.path, f"rtt{default_ext}"))
            return os.path.join(self.path, f"rtt{default_ext}"), content

        return os.path.join(self.path, f"rtt{default_ext}"), None
