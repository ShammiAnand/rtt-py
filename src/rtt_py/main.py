import typer

from .utils import log, ensure_types_match
from .services import DirWalker, UrlParser

app = typer.Typer(
    name="rtt-py",
    help="A CLI tool for easy interactions with LLMs.",
)


@app.command()
def process(
    entity: str = typer.Argument(..., help="Directory path or URL"),
    type: str = typer.Option("dir", help="Type: dir or url"),
):
    """
    Process a directory or URL and optionally query it.
    """
    if not ensure_types_match(entity, type):
        raise ValueError(
            f"entity {entity} does not match type {type}, please provide a valid entity"
        )

    if type == "dir":
        walker = DirWalker(entity)
        path = walker.convert()
        log.info(
            "finished",
            path=path,
            files_read=len(walker.files),
            entity=entity,
        )

    elif type == "url":
        url_parser = UrlParser(entity)
        path = url_parser.convert()
        log.info(
            "finished",
            path=path,
            entity=entity,
        )

    else:
        raise ValueError(
            f"unknown type {type}, please provide a valid type: dir or url"
        )


if __name__ == "__main__":
    app()
