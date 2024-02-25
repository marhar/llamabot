#!/usr/bin/env python
import duckdb
import sql_split

conn = duckdb.connect()  # Connect to an in-memory DuckDB database
def testit(input_string):
    x = sql_split.process_sql(conn, input_string)
    print(x)

# Example usage:
testit("""
This is some introductory text.
```sql
SELECT 1 as x;
```
This is some concluding text.
""")

testit("""
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
""")

testit("""
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
""")

testit("""
```sql
select 2 as y;
```
""")

testit("""
```sql
select 2 as y;
""")

testit("""
aaa
```sql
select a from foo;
```
bbb
""")

testit("""
zzz
""")
