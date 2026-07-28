import ast
import os
import subprocess
import tempfile
import textwrap


class CodeExecutor:

    @staticmethod
    def execute_python(
        code: str,
        input_data: str = "",
        function_name: str | None = None,
    ):

        temp_path = None

        try:

            wrapper = CodeExecutor.build_wrapper(
                code=code,
                input_data=input_data,
                function_name=function_name,
            )

            with tempfile.NamedTemporaryFile(
                suffix=".py",
                delete=False,
                mode="w",
                encoding="utf-8",
            ) as temp:

                temp.write(wrapper)
                temp_path = temp.name

            result = subprocess.run(
                ["python3", temp_path],
                capture_output=True,
                text=True,
                timeout=5,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "return_code": result.returncode,
            }

        except subprocess.TimeoutExpired:

            return {
                "success": False,
                "stdout": "",
                "stderr": "Execution timed out after 5 seconds.",
                "return_code": -1,
            }

        except Exception as e:

            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "return_code": -1,
            }

        finally:

            if temp_path and os.path.exists(temp_path):
                os.remove(temp_path)

    # =====================================================
    # CREATE EXECUTION WRAPPER
    # =====================================================

    @staticmethod
    def build_wrapper(
        code: str,
        input_data: str,
        function_name: str | None,
    ):

        code = textwrap.dedent(code).strip()

        # Parse input safely
        try:
            parsed_input = ast.literal_eval(input_data)
        except Exception:
            parsed_input = input_data

        # =====================================================
        # LINKED LIST QUESTIONS
        # =====================================================

        if (
            "class Node" in code
            or "class ListNode" in code
        ):

            fn = function_name or "reverse_linked_list"

            return (
                code
                + f"""

values = {repr(parsed_input)}

head = None
current = None

for value in values:
    if 'Node' in globals():
        node = Node(value)
    else:
        node = ListNode(value)

    if head is None:
        head = node
        current = node
    else:
        current.next = node
        current = node

result = {fn}(head)

output = []

while result:
    output.append(result.val)
    result = result.next

print(output)
"""
            )

        # =====================================================
        # FUNCTION QUESTIONS
        # =====================================================

        if function_name:

            return (
                code
                + f"""

data = {repr(parsed_input)}

result = {function_name}(data)

print(result)
"""
            )

        # =====================================================
        # NORMAL PROGRAM
        # =====================================================

        return code
