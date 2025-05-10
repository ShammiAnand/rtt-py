import typer


from .utils import log, ensure_types_match
from .services import DirWalker, UrlParser, ChatCompletions, InputMessage


app = typer.Typer(
    name="rtt-py",
    help="A CLI tool for easy interactions with LLMs.",
)


@app.command(
    help="Query a directory or URL using an LLM.",
)
def query(
    entity: str = typer.Argument(..., help="Directory path or URL"),
    type: str = typer.Option("dir", help="Type: dir or url"),
    query: str = typer.Option(
        "Explain the context in detail", help="Query to ask the LLM"
    ),
):
    """
    Query a directory or URL.
    """
    if not ensure_types_match(entity, type):
        raise ValueError(
            f"entity {entity} does not match type {type}, please provide a valid entity"
        )

    if type == "dir":
        walker = DirWalker(entity)
        _, content = walker.convert(want_content=True)

        log.info(
            "read directory",
            files_read=len(walker.files),
        )
        log.info(
            "querying",
            query=query,
            entity=entity,
        )

        resp, input_tokens, output_tokens = ChatCompletions().generate_response(
            InputMessage(
                **{
                    "context": content,
                    "query": query,
                }
            )
        )
        log.info(
            "finished",
            response=resp,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

    elif type == "url":
        url_parser = UrlParser(entity)
        _, content = url_parser.convert(want_content=True)

        log.info(
            "read url",
            entity=entity,
        )
        log.info(
            "querying",
            query=query,
            entity=entity,
        )

        resp, input_tokens, output_tokens = ChatCompletions().generate_response(
            InputMessage(
                **{
                    "context": content,
                    "query": query,
                }
            )
        )
        log.info(
            "finished",
            response=resp,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )


@app.command(
    help="Convert a directory or URL to markdown.",
)
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
