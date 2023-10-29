import os
import dotenv
from AIgential.modules.db import PostgresDB
from AIgential.modules import llm

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

import click

@click.command()
@click.argument('prompt')
def main(prompt):
    with PostgresDB() as db:
        db.connect_with_url(DB_URL)
        
        table_definitions = db.get_table_definitions_for_prompt()

        prompt = llm.add_cap_ref(
            prompt,
            "Here are the table definitions:", "TABLE_DEFINITIONS",
            table_definitions)
        prompt = llm.add_cap_ref(
            prompt,
            "Please provide a SQL query based on the table definitions.",
            "SQL_QUERY",
            "")

        prompt_response = llm.prompt(prompt)

        sql_query = prompt_response.split('--------')[1].strip()

        result = db.run_sql(sql_query)

        print(result)


if __name__ == "__main__":
    main()
