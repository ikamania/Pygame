def read_file(path: str) -> str:
    with open(path, "r") as file:
        text = file.read()
        file.close()
    return text


def save_file(path: str, text: str) -> bool:
    with open(path, "w") as file:
        file.write(text)
        file.close()
    return True


def round_to_value(num: int, size: int | float) -> int:
    return size * round(num / size)
