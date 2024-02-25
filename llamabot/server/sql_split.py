import duckdb

# TODO: pass in a connection to the DuckDB database
def process_sql(conn, input_string: str) -> str:
    """
    Processes an input string to find SQL blocks, executes them using DuckDB,
    and returns a string including both the SQL commands and their results.

    Parameters:
    - input_string (str): The input string containing SQL blocks and text.

    Returns:
    - str: A string with SQL blocks followed by their execution results.
    """
    lines = input_string.split('\n')
    is_sql_block = False
    buffer = []
    output_string = ""

    prefix_sql = "```sql\n"
    suffix_sql = "```\n"
    prefix_normal = "```\n"
    suffix_normal = "```\n"


    for line in lines:
        # TODO: nuke vbnet once we consistently get sql from mistral-medium
        if line.strip() in ('```sql', '```vbnet'):  # Start of SQL block
            if not is_sql_block:  # Only switch mode if not already in a SQL block
                is_sql_block = True
                if buffer:  # If there's text in the buffer, append it first
                    output_string += '\n'.join(buffer) + '\n'
                    buffer = []
        elif line.strip() == '```' and is_sql_block:  # End of SQL block
            is_sql_block = False
            sql_query = '\n'.join(buffer)
            output_string += prefix_sql
            output_string += sql_query + '\n'
            output_string += suffix_sql


            try:
                # TODO: if it's an insert, then select the rows?
                result = conn.sql(sql_query)
                if result:
                    output_string += prefix_normal
                    output_string += str(result)
                    output_string += suffix_normal
            except Exception as e:
                output_string += prefix_normal
                output_string += 'SQL Execution Error: ' + str(e) + '\n'
                output_string += suffix_normal
            buffer = []
        else:
            buffer.append(line)

    # Add remaining content
    if buffer:
        if is_sql_block:  # If still in an SQL block, try to execute
            output_string += prefix_sql
            sql_query = '\n'.join(buffer)
            output_string += suffix_sql
            output_string += prefix_normal
            try:
                result = conn.sql(sql_query)
                output_string += sql_query + '\n' + str(result) + '\n'
            except Exception as e:
                output_string += 'SQL Execution Error: ' + str(e) + '\n'
            output_string += suffix_normal
        else:  # If not, just append the text
            output_string += '\n'.join(buffer) + '\n'

    return output_string
