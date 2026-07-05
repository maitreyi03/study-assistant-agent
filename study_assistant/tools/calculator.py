"""A restricted calculator tool for the study assistant agent."""

import ast
import operator
from collections.abc import Callable

from langchain.tools import tool


BinaryOperation = Callable[[int | float, int | float], int | float]
UnaryOperation = Callable[[int | float], int | float]

ALLOWED_BINARY_OPERATORS: dict[type[ast.operator], BinaryOperation] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

ALLOWED_UNARY_OPERATORS: dict[type[ast.unaryop], UnaryOperation] = {
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def evaluate_math_node(node: ast.AST) -> int | float:
    """Recursively evaluate a restricted mathematical expression."""
    if isinstance(node, ast.Constant):
        if isinstance(node.value, bool):
            raise ValueError("Boolean values are not supported.")

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are supported.")

    if isinstance(node, ast.BinOp):
        operation = ALLOWED_BINARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("That mathematical operation is not supported.")

        left = evaluate_math_node(node.left)
        right = evaluate_math_node(node.right)

        if isinstance(node.op, ast.Pow) and abs(right) > 100:
            raise ValueError("The exponent is too large.")

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):
        operation = ALLOWED_UNARY_OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("That unary operation is not supported.")

        return operation(evaluate_math_node(node.operand))

    raise ValueError("The expression contains unsupported content.")


@tool
def calculator(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Examples:
    - 25 * 4
    - (10 + 5) / 3
    - 2 ** 8
    """
    try:
        parsed_expression = ast.parse(expression, mode="eval")
        answer = evaluate_math_node(parsed_expression.body)
        return str(answer)
    except (SyntaxError, ValueError, ZeroDivisionError, OverflowError) as error:
        return f"Could not calculate the expression: {error}"
