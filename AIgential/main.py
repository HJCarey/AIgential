"""
Entrypoint for the Autogen Experiments package.
"""
import logging
import click

from autogen_experiments import research_agent as ae_research_agent

##################
# Research Agent #
##################
@click.group()
def cli_research_agent():
    """Research Agent"""
    pass

@cli_research_agent.command()
@click.option(
    "--task",
    help="Task for the agent to research.",
    type=str,
    default="How does OPENAI work?",
)
def research_agent(task):
    """Research Agent"""
    logging.info("Running research_agent...")

    ae_research_agent.research(
        task
    )

##################
# CLI Collection #
##################
cli = click.CommandCollection(
    sources=[
        cli_research_agent,
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