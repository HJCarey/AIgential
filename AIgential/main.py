import os
import dotenv
from AIgential.modules.db import PostgresDB
from AIgential.modules import llm

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

def main():
    # parse prompt param using click

    # connect to db using with statement and create a db_manager
    with PostgresDB() as db:
        db.connect_with_url(DB_URL)
        
        users_table = db.get_all("playing_with_neon")

        print("users_table", users_table)

    # call db_manager.get_table_definition_for_prompt() to et tables in prompt ready form

    # create two blank calls to llm.add_cap_ref() that update our curren tprompt passed in from cli

    # call llm.prompt to et a prompt_response variable

    # parse sql response from prompt_response using SQL_QUERY_DELIMITER '--------'

    # call db_manager.run_sql() with the parsed sql

    pass


if __name__ == "__main__":
    main()