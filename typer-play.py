import typer

app = typer.Typer()

@app.command()
def hello(name: str):
    typer.echo((f"hh {name}"))

@app.command()
def addition(num: int, num2: int):
    typer.echo(num+num2)

if __name__ == "__main__":
    app()



------


def main(
        sourceCSV: str = typer.Argument(..., help="The CSV from the car logger"),
        destSheet: str = typer.Argument(..., help="The spreadsheet to output on"), # TODO Spreadsheet must exist for now
        startDate: str = typer.Argument('2021-06-30'), # TODO Allow autodetect year in future
        endDate: str = typer.Argument('2022-06-01')
        ):
    """
    A program that calculates work travel.\n
    Dates default to financial year at time of writing.
    """

    dRange = [startDate, endDate]

    typer.echo(f"Hello {sourceCSV}")
    #typer.echo(destSheet, startDate, endDate)


if __name__ == "__main__":
    typer.run(main)