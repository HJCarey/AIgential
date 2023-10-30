import os
import dotenv
from AIgential.modules.db import PostgresDB
from AIgential.modules import llm

dotenv.load_dotenv()

assert os.environ.get("DATABASE_URL"), "POSTGRES_CONNECTION_URL not found in .env file"
assert os.environ.get("OPENAI_API_KEY"), "OPENAI_API_KEY not found in .env file"

DB_URL = os.environ.get("DATABASE_URL")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

POSTGRES_TABLE_DEFINITIONS_CAP_REF = "TABLE_DEFINITIONS"
RESPONSE_FORMAT_CAP_REF = "RESPONSE_FORMAT"

SQL_DELIMETER = "--------"

def main(args):
    prompt = args["prompt"]
    with PostgresDB() as db:
        print("prompt v1", prompt)

        db.connect_with_url(DB_URL)
        
        table_definitions = db.get_table_definitions_for_prompt()

        print("table_definitions", table_definitions)
        

        prompt = llm.add_cap_ref(
            prompt,
            f"Use these {POSTGRES_TABLE_DEFINITIONS_CAP_REF} to satisfy th edatabase query.",
            POSTGRES_TABLE_DEFINITIONS_CAP_REF,
            table_definitions
        )
        
        print("prompt v2", prompt)

        prompt = llm.add_cap_ref(
            prompt,
            f"\n\nI want to directly extract the sql query from your response. Follow the instructions strictly, Respond exactly in this format {RESPONSE_FORMAT_CAP_REF} where you should replace the question in the <> with the value.",
            RESPONSE_FORMAT_CAP_REF,
            f"""<explanation of sql query>
            < replace the <> with only sql query, no other instructions after the following delimiters -------- >
{SQL_DELIMETER}
<>""",
        )

        print("prompt v3", prompt)

        prompt_response = llm.prompt(prompt)

        print('prompt_response', prompt_response)

        sql_query = prompt_response.split(SQL_DELIMETER)[1].strip()

        print("sql_query", sql_query)

        result = db.run_sql(sql_query)

        print("-------- POSTGRES DATA ANALYTICS AI AGENT RESPONSE --------")

        print(result)


if __name__ == "__main__":
    main()
