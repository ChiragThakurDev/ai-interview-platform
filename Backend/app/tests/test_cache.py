from app.ai.cache import CacheManager


def test_set_get():

    cache = CacheManager()

    cache.set(
        "hello",
        "world",
    )

    assert cache.get("hello") == "world"


def test_exists():

    cache = CacheManager()

    cache.set(
        "test",
        123,
    )

    assert cache.exists("test")


def test_delete():

    cache = CacheManager()

    cache.set(
        "temp",
        "abc",
    )

    cache.delete(
        "temp"
    )

    assert cache.get("temp") is None


def test_json():

    cache = CacheManager()

    cache.set(
        "user",
        {
            "name": "Chirag",
            "role": "AI Engineer",
        },
    )

    assert cache.get("user")["name"] == "Chirag"
