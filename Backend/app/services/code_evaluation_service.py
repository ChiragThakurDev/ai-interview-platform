from app.services.ai_service import AIService
from app.utils.code_executor import CodeExecutor


class CodeEvaluationService:

    def __init__(self):
        self.ai_service = AIService()

    def evaluate(
        self,
        question,
        language: str,
        code: str,
        test_cases: list,
    ):

        results = []

        passed_tests = 0

        for test_case in test_cases:

            execution = CodeExecutor.execute_python(
                code=code,
                input_data=test_case.input_data,
            )

            actual_output = execution["stdout"].strip()

            expected_output = test_case.expected_output.strip()

            passed = (
                execution["success"]
                and actual_output == expected_output
            )

            if passed:
                passed_tests += 1

            results.append(
                {
                    "input": test_case.input_data,
                    "expected": expected_output,
                    "actual": actual_output,
                    "passed": passed,
                    "stderr": execution["stderr"],
                }
            )

        return {
            "passed_tests": passed_tests,
            "total_tests": len(test_cases),
            "results": results,
        }
