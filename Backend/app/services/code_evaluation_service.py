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
                function_name=question.function_name,
            )

            actual_output = execution.get("stdout", "").strip()
            expected_output = test_case.expected_output.strip()

            passed = (
                execution.get("success", False)
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
                    "stderr": execution.get("stderr", ""),
                }
            )

        total_tests = len(test_cases)

        overall_passed = (
            total_tests > 0
            and passed_tests == total_tests
        )

        score = (
            int((passed_tests / total_tests) * 100)
            if total_tests
            else 0
        )

        feedback = (
            "All test cases passed. Excellent solution."
            if overall_passed
            else f"Passed {passed_tests}/{total_tests} test cases. Improve your solution."
        )

        # Simple heuristic values until AI evaluation is added
        correctness = score
        code_quality = score

        if score == 100:
            time_complexity = "Optimal"
            space_complexity = "Optimal"
        else:
            time_complexity = "Unknown"
            space_complexity = "Unknown"

        strengths = []
        weaknesses = []
        bugs = []
        optimization_suggestions = []

        if overall_passed:
            strengths.append("All test cases passed")
            strengths.append("Correct output produced")
        else:
            weaknesses.append("Failed one or more test cases")

            for result in results:
                if result["stderr"]:
                    bugs.append(result["stderr"])
                    break

            optimization_suggestions.append(
                "Handle all edge cases and ensure the function returns the expected output."
            )

        return {
            "passed": overall_passed,
            "score": score,
            "correctness": correctness,
            "code_quality": code_quality,
            "time_complexity": time_complexity,
            "space_complexity": space_complexity,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "bugs": bugs,
            "optimization_suggestions": optimization_suggestions,
            "feedback": feedback,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "results": results,
        }
