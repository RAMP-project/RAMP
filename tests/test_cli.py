import os
import shutil

import mock
import matplotlib.pyplot as plt
import pytest
from ramp.cli import parser as ramp_parser, main as ramp_main
from .utils import TEST_PATH, TEST_OUTPUT_PATH


class TestProcessUserArguments:
    def setup_method(self):
        if os.path.exists(TEST_OUTPUT_PATH):
            shutil.rmtree(TEST_OUTPUT_PATH, ignore_errors=True)
        if os.path.exists(TEST_OUTPUT_PATH) is False:
            os.mkdir(TEST_OUTPUT_PATH)

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=ramp_parser.parse_args(
            ["--start-date", "2022-01-01", "-y", "2022"]
        ),
    )
    def test_impossible_option_combinaison_start_date_year(self, m_args):
        with pytest.raises(ValueError):
            ramp_main()

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=ramp_parser.parse_args(["--end-date", "2022-01-01", "-y", "2022"]),
    )
    def test_impossible_option_combinaison_end_date_year(self, m_args):
        with pytest.raises(ValueError):
            ramp_main()

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=ramp_parser.parse_args(
            [
                "-i",
                os.path.join(TEST_PATH, "test_inputs", "example_excel_usecase.xlsx"),
                "-y",
                "2022",
                "2023",
                "-o",
                os.path.join(TEST_OUTPUT_PATH, "example_excel.csv"),
            ]
        ),
    )
    def test_multiple_year_is_possible(self, m_args, monkeypatch):
        monkeypatch.setattr(
            plt, "show", lambda: None
        )  # prevents the test to output figure
        ramp_main()

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=ramp_parser.parse_args(
            [
                "-i",
                os.path.join(TEST_OUTPUT_PATH),
                "-y",
                "2022",
                "-n",
                "1",
            ]
        ),
    )
    def test_month_variation_without_month_files(self, m_args):
        with pytest.raises(ValueError):
            ramp_main()

    @mock.patch(
        "argparse.ArgumentParser.parse_args",
        return_value=ramp_parser.parse_args(
            [
                "-i",
                os.path.join(TEST_OUTPUT_PATH),
                "-y",
                "2022",
                "-n",
                "1",
            ]
        ),
    )
    def test_month_variation_with_month_files(self, m_args):
        for i in range(12):
            shutil.copy(
                os.path.join(TEST_PATH, "test_inputs", "example_excel_usecase.xlsx"),
                os.path.join(TEST_OUTPUT_PATH, f"example_excel_usecase_{i}.xlsx"),
            )
        ramp_main()

    def teardown_method(self):
        if os.path.exists(TEST_OUTPUT_PATH):
            shutil.rmtree(TEST_OUTPUT_PATH, ignore_errors=True)
