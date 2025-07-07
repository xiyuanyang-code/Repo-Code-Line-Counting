import code_counter.cli as cnt


def test_simple():
    result = cnt.count_code_lines("../")
    assert type(result) == type((1, 2, 3))

    print(result)
    print(result[-1].keys())
    code_type = list(result[-1].keys())
    code_type = [type_element[1:] for type_element in code_type]
    print("Code types: {}".format(", ".join(code_type)))


if __name__ == "__main__":
    test_simple()
