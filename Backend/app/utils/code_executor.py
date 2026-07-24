import os
import tempfile
import subprocess


class CodeExecutor:

    @staticmethod
    def execute_python(code: str):

        temp_path = None

        try:
            with tempfile.NamedTemporaryFile(
                suffix=".py",
                delete=False,
                mode="w",
            ) as temp:

                temp.write(code)
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
