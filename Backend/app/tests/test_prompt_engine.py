from app.ai.prompt_manager import PromptManager


def test_prompt_build():

    prompt = PromptManager.build(
        "chat",
        name="Chirag",
        question="Explain OOP"
    )

    assert "Chirag" in prompt
    assert "Explain OOP" in prompt


def test_prompt_contains_system_text():

    prompt = PromptManager.build(
        "chat",
        name="A",
        question="B",
    )

    assert "AI Interview Assistant" in prompt
