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

        # =====================================================
        # NON-PYTHON: STATIC AI EVALUATION
        # =====================================================
        # The Docker container does not ship with heavy compilers (g++, javac).
        # We rely on the highly capable coding model to statically grade the
        # logic and correctness of non-Python submissions.
        if language.lower() not in ["python", "python3"]:
            question_context = f"Title: {question.title}\nDesc: {question.description}\nTest Cases:\n"
            for t in test_cases:
                question_context += f"Input: {t.input_data} -> Expected: {t.expected_output}\n"

            ai_result = self.ai_service.evaluate_code(
                question=question_context,
                language=language,
                code=code,
                execution_output="Skipped local execution (Language not supported locally). Evaluate correctness statically.",
                execution_error="None",
            )

            # Ensure AI result conforms to expected dictionary structure
            if not isinstance(ai_result, dict):
                ai_result = {}

            # Score is 0-10 in prompt, but we scale it to 0-100 to match DB schema
            def scale_out_of_100(val, fallback):
                if val is None:
                    val = fallback
                try:
                    val = float(val)
                except (ValueError, TypeError):
                    val = 0
                return int(val * 10) if val <= 10 else int(val)

            raw_score = ai_result.get("score", 0)
            ai_score = scale_out_of_100(raw_score, 0)
            correctness = scale_out_of_100(ai_result.get("correctness"), raw_score)
            code_quality = scale_out_of_100(ai_result.get("code_quality"), raw_score)

            return {
                "passed": ai_result.get("passed", False),
                "score": ai_score,
                "correctness": correctness,
                "code_quality": code_quality,
                "time_complexity": ai_result.get("time_complexity", "Unknown"),
                "space_complexity": ai_result.get("space_complexity", "Unknown"),
                "strengths": ai_result.get("strengths", []),
                "weaknesses": ai_result.get("weaknesses", []),
                "bugs": ai_result.get("bugs", []),
                "optimization_suggestions": ai_result.get("optimization_suggestions", []),
                "feedback": ai_result.get("feedback", "Code was evaluated successfully."),
                "passed_tests": 0,
                "total_tests": len(test_cases),
                "results": [],
            }

        # =====================================================
        # PYTHON: LOCAL SANDBOX EXECUTION
        # =====================================================
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
        overall_passed = (total_tests > 0 and passed_tests == total_tests)
        score = int((passed_tests / total_tests) * 100) if total_tests else 0

        feedback = (
            "All test cases passed. Excellent solution."
            if overall_passed
            else f"Passed {passed_tests}/{total_tests} test cases. Improve your solution."
        )

        strengths = ["All test cases passed", "Correct output produced"] if overall_passed else []
        weaknesses = ["Failed one or more test cases"] if not overall_passed else []
        bugs = []
        optimization_suggestions = []

        if not overall_passed:
            for result in results:
                if result["stderr"]:
                    bugs.append(result["stderr"])
                    break
            optimization_suggestions.append("Handle all edge cases and ensure the function returns the expected output.")

        return {
            "passed": overall_passed,
            "score": score,
            "correctness": score,
            "code_quality": score,
            "time_complexity": "Optimal" if score == 100 else "Unknown",
            "space_complexity": "Optimal" if score == 100 else "Unknown",
            "strengths": strengths,
            "weaknesses": weaknesses,
            "bugs": bugs,
            "optimization_suggestions": optimization_suggestions,
            "feedback": feedback,
            "passed_tests": passed_tests,
            "total_tests": total_tests,
            "results": results,
        }
