import typer

from .utils import log, ensure_types_match
from .services import DirWalker, UrlParser


def cli(
    entity: str,  # the entity can be a directory path or an url
    type: str = "dir",  # the type can be dir or url
    query: str
    | None = None,  # the query is the question you want to ask to llm about the entity
) -> None:
    """
    this is an entrypoint for the cli, it will be used to read a repo or url
    """

    log.info("cli", entity=entity, type=type)

    if not ensure_types_match(entity, type):
        raise ValueError(
            f"entity {entity} does not match type {type}, please provide a valid entity"
        )

    if type == "dir":
        walker = DirWalker(entity)
        path = walker.convert()
        log.info("output stored", path=path, files_read=len(walker.files))
    elif type == "url":
        url_parser = UrlParser(entity)
        path = url_parser.convert()
        log.info("output stored", path=path)
    else:
        raise ValueError(
            f"unknown type {type}, please provide a valid type: dir or url"
        )


if __name__ == "__main__":
    typer.run(cli)
