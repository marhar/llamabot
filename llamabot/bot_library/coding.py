"""Prompts and bots for coding.

codebot is an instance of SimpleBot.
The way to use codebot is as follows:

```python
prompt = "..." # some string
output = codebot(prompt)
```

Prompts are composed from the python functions that are inside here.
So we can do something like:

```python
output = codebot(one_of_these_functions(argument))
```
"""

import outlines.text as text

from llamabot.bot.simplebot import SimpleBot

codebot = SimpleBot(
    """You are a Python programming expert.

You provide suggestions to programmers in Python.

Only return code, do not put Markdown syntax in your output.
Do not explain your code, only provide code.

Code should have type hints.
Ensure that the implementation of the function results in the simplest type hints possible.

Ensure that within any errors raised, the error message is actionable
and informs the user what they need to do to fix the error.
Make sure the error message is prescriptive,
possibly even more verbose than necessary,
and includes verbiage such as "please do X" or "please do not do Y".

If you are called to suggest docstrings, you always use the sphinx-style docstrings.

If you are asked to write tests, prefer the use of Hypothesis to generate property-based tests.
Only suggest example-based tests if it is not possible to generate property-based tests.
For each test, please write a docstring that explains what the test is testing.
For test function style, use pytest-style test functions and not Unittest-style test classes.
"""
)


@text.prompt
def ghostwriter(desired_functionality):
    """I would like to accomplish the following.

    {{ desired_functionality }}

    How do I write the code for this? Please return only the code without explaining it.

    Ensure that there are type hints in the function.

    # noqa: DAR101
    """


@text.prompt
def docstring(code):
    """Please help me write docstrings for the following code.

    Ensure that you use Markdown Python block(s) to showcase how the code should be used.
    The code usage example should be before the parameter/argument documentation.
    Do not use sphinx-style directives,
    but instead use Markdown-style triple back-ticks to house the code block.

    Do not include :type: or :rtype: in the docstring
    as they should be covered by the type hints.

    {{ code }}

    # noqa: DAR101
    """


@text.prompt
def tests(code):
    """Please help me write unit tests for the following code.

    {{ code }}

    # noqa: DAR101
    """
