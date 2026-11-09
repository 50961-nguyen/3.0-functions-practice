import pytest
import ast
import inspect
import textwrap

# ── helpers ──────────────────────────────────────────────────────────────────

def _source() -> str:
    with open("func_practice.py", "r") as f:
        return f.read()

def _module_docstring() -> str:
    """Return the module-level string (first statement if it's a string literal)."""
    tree = ast.parse(_source())
    return ast.get_docstring(tree) or ""

def _func_docstring(func_name: str) -> str:
    tree = ast.parse(_source())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return ast.get_docstring(node) or ""
    return ""

def _func_source(func_name: str) -> str:
    tree = ast.parse(_source())
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return ast.get_source_segment(_source(), node) or ""
    return ""

# ── header comment tests ──────────────────────────────────────────────────────

class TestHeaderComments:
    """The file must open with a module-level docstring containing author & date."""

    def test_header_exists(self):
        """A module-level docstring / header comment block must be present."""
        header = _module_docstring()
        assert header.strip(), (
            "Missing module-level header comment. "
            'Add a triple-quoted string at the very top of func_practice.py with '
            'author, date, and a short description.'
        )

    def test_header_has_author(self):
        header = _module_docstring().lower()
        assert "author" in header, (
            "Header comment is missing an 'author' line. "
            "Example:  author: Your Name"
        )

    def test_header_has_date(self):
        header = _module_docstring().lower()
        assert "date" in header, (
            "Header comment is missing a 'date' line. "
            "Example:  date: April 1, 2026"
        )

    def test_header_has_description(self):
        """Header must contain at least one non-field descriptive line."""
        lines = [
            ln.strip()
            for ln in _module_docstring().splitlines()
            if ln.strip() and not ln.lower().lstrip().startswith(("author", "date"))
        ]
        assert lines, (
            "Header comment should include a short description of the file, "
            "e.g. 'Practicing with functions'."
        )

# ── docstring tests ───────────────────────────────────────────────────────────

class TestDocstrings:
    """Every function must have a properly formatted NumPy/Google-style docstring."""

    @pytest.mark.parametrize("func_name", ["evenly_divides", "is_prime"])
    def test_docstring_exists(self, func_name):
        ds = _func_docstring(func_name)
        assert ds.strip(), (
            f"Function '{func_name}' is missing a docstring. "
            "Add a triple-quoted string as the very first statement of the function."
        )

    def test_main_docstring_exists(self):
        ds = _func_docstring("main")
        assert ds.strip(), (
            "main() is missing a docstring. "
            "Add a triple-quoted string as the very first statement describing what main does."
        )

    @pytest.mark.parametrize("func_name", ["evenly_divides", "is_prime"])
    def test_docstring_has_args_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "args:" in ds or "arguments:" in ds or "parameters:" in ds, (
            f"Docstring for '{func_name}' is missing an 'Args:' section. "
            "Document each parameter with its type and description."
        )

    @pytest.mark.parametrize("func_name", ["evenly_divides", "is_prime"])
    def test_docstring_has_returns_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "returns:" in ds or "return:" in ds, (
            f"Docstring for '{func_name}' is missing a 'Returns:' section. "
            "Describe what the function returns and its type."
        )

    @pytest.mark.parametrize("func_name", ["evenly_divides", "is_prime"])
    def test_docstring_has_example_section(self, func_name):
        ds = _func_docstring(func_name).lower()
        assert "example" in ds, (
            f"Docstring for '{func_name}' is missing an 'Example' or 'Examples:' section. "
            "Show at least one sample call and its expected output."
        )

    @pytest.mark.parametrize("func_name", ["evenly_divides", "is_prime"])
    def test_docstring_has_description(self, func_name):
        """First non-blank line of the docstring should be a plain-English description."""
        ds = _func_docstring(func_name)
        first_line = next(
            (ln.strip() for ln in ds.splitlines() if ln.strip()), ""
        )
        assert first_line and first_line.lower() not in ("args:", "returns:", "example:", "examples:"), (
            f"Docstring for '{func_name}' should start with a one-line description "
            "of what the function does before listing Args/Returns/Example."
        )

# ── IPO comment tests ─────────────────────────────────────────────────────────

class TestIPOComments:
    """main() must contain Input, Processing, and Output comment markers."""

    def _main_source(self) -> str:
        return _func_source("main")

    def test_ipo_input_comment(self):
        src = self._main_source().lower()
        assert "# input" in src, (
            "main() is missing an '# Input' comment. "
            "Mark the section where you read user input with '# Input'."
        )

    def test_ipo_processing_comment(self):
        src = self._main_source().lower()
        has_processing = "# processing" in src
        assert has_processing, (
            "main() is missing a '# Processing' (or '# Processing/Output') comment. "
            "Mark the section where you process data with '# Processing'."
        )

    def test_ipo_output_comment(self):
        src = self._main_source().lower()
        # Accept either a dedicated "# output" line or a combined "# processing/output"
        has_output = "# output" in src or "# processing/output" in src
        assert has_output, (
            "main() is missing an '# Output' comment. "
            "Mark where output is printed with '# Output' or combine it as '# Processing/Output'."
        )

# ── functionality tests (unchanged) ──────────────────────────────────────────

@pytest.mark.parametrize("a,b,result", [
    (2, 4, True),
    (4, 2, False),
    (6, 36, True),
    (7, 36, False),
])
def test_evenly_divides(a, b, result):
    from func_practice import evenly_divides

    assert evenly_divides(a, b) == result

@pytest.mark.parametrize("a,result", [
    (2, True),
    (4, False),
    (17, True),
    (357, False)
])
def test_is_prime(a, result):
    from func_practice import is_prime

    assert is_prime(a) == result

def test_main(capsys, monkeypatch):
    from func_practice import main

    monkeypatch.setattr("builtins.input", lambda _: "17")
    main()
    captured = capsys.readouterr()
    assert "17 is prime" in captured.out