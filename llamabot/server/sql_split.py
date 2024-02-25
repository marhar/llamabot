import duckdb

def process_sql(input_string):
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

    conn = duckdb.connect()  # Connect to an in-memory DuckDB database

    for line in lines:
        if line.strip() == '```sql':  # Start of SQL block
            if not is_sql_block:  # Only switch mode if not already in a SQL block
                is_sql_block = True
                if buffer:  # If there's text in the buffer, append it first
                    output_string += '\n'.join(buffer) + '\n'
                    buffer = []
        elif line.strip() == '```' and is_sql_block:  # End of SQL block
            is_sql_block = False
            sql_query = '\n'.join(buffer)
            output_string += sql_query + '\n'

            try:
                result = conn.sql(sql_query)
                output_string += str(result) + '\n'
            except Exception as e:
                output_string += 'SQL Execution Error: ' + str(e) + '\n'
            buffer = []
        else:
            buffer.append(line)

    # Add remaining content
    if buffer:
        if is_sql_block:  # If still in an SQL block, try to execute
            sql_query = '\n'.join(buffer)
            try:
                result = conn.sql(sql_query)
                output_string += sql_query + '\n' + str(result) + '\n'
            except Exception as e:
                output_string += 'SQL Execution Error: ' + str(e) + '\n'
        else:  # If not, just append the text
            output_string += '\n'.join(buffer) + '\n'

    conn.close()  # Close the database connection
    return output_string
