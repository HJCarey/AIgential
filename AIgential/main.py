"""
Entrypoint for the Autogen Experiments package.
"""
import logging
import click

from AIgential import postgres_agent as ai_postgres_agent

##################
# Postgres Agent #
##################
@click.group()
def cli_postgres_agent():
    """Postgres Agent"""
    pass

@cli_postgres_agent.command()
@click.option(
    "--prompt",
    help="Prompt for the Postgres agent to do.",
    type=str,
    default="Give me the first 10 users in alphabetical order.",
)
def postgres_agent(prompt):
    """Postgres Agent"""
    logging.info("Running postgres_agent...")

    args = {
        "prompt": prompt,
    }

    ai_postgres_agent.main(args)

##################
# CLI Collection #
##################
cli = click.CommandCollection(
    sources=[
        cli_postgres_agent,
    ]
)

##################
# CLI Entrypoint #
##################
if __name__ == "__main__":
    logging.basicConfig(
        format="[ %(asctime)s.%(msecs)03d - %(levelname)s - %(filename)s:%(lineno)d ] %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    cli()