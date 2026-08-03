"""
Prompt Version Registry.

Keeps track of the latest version for every prompt category.

Changing a version here updates the entire application.
"""


PROMPT_VERSIONS = {
    "chat": "v1",
    "coding": "v1",
    "resume": "v1",
    "interview": "v1",
    "roadmap": "v1",
    "system": "v1",
}


def get_prompt_version(prompt_type: str) -> str:
    """
    Returns the active version for a prompt type.
    """

    return PROMPT_VERSIONS.get(prompt_type, "v1")


def set_prompt_version(prompt_type: str, version: str):
    """
    Updates the active version.
    """

    PROMPT_VERSIONS[prompt_type] = version
