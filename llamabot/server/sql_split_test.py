#!/usr/bin/env python
import duckdb
import sql_split

# Example usage:
input_string = """
This is some introductory text.
```sql
SELECT 1 as x;
```
This is some concluding text.
"""
x = sql_split.process_sql(input_string)
print(x)

input_string = """
aaa
```sql
SELECT 1 as x;
```
bbb
```sql
select 2 as y;
```
ccc
```
ddd
```
eee
"""
x = sql_split.process_sql(input_string)
print(x)

input_string = """
aaa
```sql
SELECT 1 as x;
```
bbb
```sql
select 2 as y;
```
ccc
```
ddd
```
eee
"""
x = sql_split.process_sql(input_string)
print(x)

input_string = """
```sql
select 2 as y;
```
"""
x = sql_split.process_sql(input_string)
print(x)

input_string = """
```sql
select 2 as y;
"""
x = sql_split.process_sql(input_string)
print(x)

input_string = """
aaa
```sql
select a from foo;
```
bbb
"""
x = sql_split.process_sql(input_string)
print(x)
