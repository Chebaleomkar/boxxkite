import os


def pytest_generate_tests(metafunc):
    if "repeat_i" in metafunc.fixturenames:
        metafunc.parametrize("repeat_i", range(int(os.environ.get("REPEAT", "200"))))
