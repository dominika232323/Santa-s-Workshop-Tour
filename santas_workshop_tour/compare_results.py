from pathlib import Path

import typer

from santas_workshop_tour.results_handler import is_result_valid


app = typer.Typer()


@app.command()
def main(list_of_results: list[Path]):
    for result_path in list_of_results:
        is_result_valid(result_path)



if __name__ == "__main__":
    app()
