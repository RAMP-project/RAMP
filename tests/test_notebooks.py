import os
import pytest
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor, CellExecutionError

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NB_DIR = os.path.join(BASE_DIR, "docs", "notebooks")

NOTEBOOKS = [f for f in os.listdir(NB_DIR) if f.endswith(".ipynb")]


class TestJupyterNotebooksInDocumentation:
    def setup_method(self):
        self.ep = ExecutePreprocessor(timeout=600, kernel_name="python3")

    @pytest.mark.parametrize("notebook", NOTEBOOKS)
    def test_example_notebook_runs_though(self, notebook):
        notebook_filename = os.path.join(NB_DIR, notebook)
        with open(notebook_filename) as f:
            nb = nbformat.read(f, as_version=4)
        try:
            self.ep.preprocess(nb, {"metadata": {"path": NB_DIR}})
        except CellExecutionError:
            with open(
                os.path.join(".", "errored_" + notebook), mode="w", encoding="utf-8"
            ) as f:
                nbformat.write(nb, f)
            pytest.fail(f"Notebook {notebook} did not run through without error")
