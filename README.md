# Code Line Counting Tool

This tool counts the number of code lines in a repository, with options to ignore specific folders and filter by file extensions. It logs detailed results to both the console and a log file.

## Usage

```bash
# after cloning the repo
cd Repo-Code-Line-Counting
pip install .
```

Then you can use this module in your code!

```python
import code_counter.cli as cnt


def test_simple():
    result = cnt.count_code_lines("../")
    assert type(result) == type((1, 2, 3))

    print(result[-1].keys())
    code_type = list(result[-1].keys())
    code_type = [type_element[1:] for type_element in code_type]
    print("Code types: {}".format(", ".join(code_type)))


if __name__ == "__main__":
    test_simple()
```

## Log Output Example

```python
>>> # result is generated in the code section above.
>>> print(result)
(20886, {'.md': 887, '.txt': 312, '.cpp': 303, '.py': 838, '.tex': 356, '.html': 511, '.yml': 58, '.json': 5448, '.TAG': 4, '.ipynb': 131, '.js': 352, '.sh': 210, '.css': 10972, '.scss': 251, '.pug': 253})
dict_keys(['.md', '.txt', '.cpp', '.py', '.tex', '.html', '.yml', '.json', '.TAG', '.ipynb', '.js', '.sh', '.css', '.scss', '.pug'])
```

## Todo 

- integrate `.gitignore` file directly.

- add GUI interface.

- add more tests.