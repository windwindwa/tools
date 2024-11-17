# python
# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 11/17/24 00:46
# @Author  : lzg
# @Site    : 
# @File    : test_append_to_excel.py
# @Software: PyCharm
import pytest
import os
import pandas as pd
from tempfile import NamedTemporaryFile
from findReviewer.useDerison.justtest import append_to_excel
import pytest
import os
import pandas as pd
from tempfile import TemporaryDirectory


# Ensure `ensure_excel_file_with_headers` is already defined

def test_append_to_excel_create_and_append():
    """
    Test if the function creates the file and appends data when the file does not exist.
    """
    target_result = [
        {
            'name': 'T Sharma',
            'href': '/citations?user=U_iQbMIAAAAJ&hl=zh-CN&oi=sra',
            'profile_info': {
                'affiliation': 'Penn State University',
                'position': 'Assistant Professor',
            }
        }
    ]

    with TemporaryDirectory() as temp_dir:
        file_name = "test_append_creation.xlsx"
        full_path = os.path.join(temp_dir, file_name)

        # Test when the file does not exist
        append_to_excel(target_result, temp_dir, file_name)

        # Check if the file is created
        assert os.path.exists(full_path), "The file should be created if it doesn't exist."

        # Check the content of the file
        df = pd.read_excel(full_path)
        assert len(df) == 1, "The file should contain one row."
        assert df.iloc[0]["Name"] == "T Sharma", "The Name column should be correctly filled."
        assert df.iloc[0][
                   "Affiliation"] == "Penn State University", "The Affiliation column should be correctly filled."
        assert df.iloc[0][
                   "Choice Reason"] == "Assistant Professor", "The Choice Reason column should be correctly filled."
        assert df.iloc[0]["Google Scholar Home Page"] == "/citations?user=U_iQbMIAAAAJ&hl=zh-CN&oi=sra", \
            "The Google Scholar Home Page column should be correctly filled."


def test_append_to_excel_append_existing_file():
    """
    Test if the function appends data when the file already exists.
    """
    initial_data = pd.DataFrame(columns=["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"])
    target_result = [
        {
            'name': 'A Smith',
            'href': '/citations?user=A123&hl=zh-CN&oi=sra',
            'profile_info': {
                'affiliation': 'MIT',
                'position': 'Associate Professor',
            }
        }
    ]

    with TemporaryDirectory() as temp_dir:
        file_name = "test_append_existing.xlsx"
        full_path = os.path.join(temp_dir, file_name)

        # Create initial file
        initial_data.to_excel(full_path, index=False)

        # Append data to the existing file
        append_to_excel(target_result, temp_dir, file_name)

        # Check the content of the file
        df = pd.read_excel(full_path)
        assert len(df) == 1, "The file should contain one row after appending."
        assert df.iloc[0]["Name"] == "A Smith", "The Name column should be correctly filled."
        assert df.iloc[0]["Affiliation"] == "MIT", "The Affiliation column should be correctly filled."
        assert df.iloc[0][
                   "Choice Reason"] == "Associate Professor", "The Choice Reason column should be correctly filled."
        assert df.iloc[0]["Google Scholar Home Page"] == "/citations?user=A123&hl=zh-CN&oi=sra", \
            "The Google Scholar Home Page column should be correctly filled."


def test_append_to_excel_fix_invalid_headers():
    """
    Test if the function fixes headers and appends data when the file has invalid headers.
    """
    invalid_data = pd.DataFrame(columns=["InvalidColumn"])
    target_result = [
        {
            'name': 'B Johnson',
            'href': '/citations?user=B456&hl=zh-CN&oi=sra',
            'profile_info': {
                'affiliation': 'Stanford',
                'position': 'Professor',
            }
        }
    ]

    with TemporaryDirectory() as temp_dir:
        file_name = "test_append_invalid_headers.xlsx"
        full_path = os.path.join(temp_dir, file_name)

        # Create a file with invalid headers
        invalid_data.to_excel(full_path, index=False)

        # Call append_to_excel to fix headers and append data
        append_to_excel(target_result, temp_dir, file_name)

        # Check the content of the file
        df = pd.read_excel(full_path)
        assert len(df) == 1, "The file should contain one row after fixing headers and appending."
        assert list(df.columns) == ["Name", "Affiliation", "Email", "Choice Reason", "Google Scholar Home Page"], \
            "The headers should be fixed to match the required columns."
        assert df.iloc[0]["Name"] == "B Johnson", "The Name column should be correctly filled."
        assert df.iloc[0]["Affiliation"] == "Stanford", "The Affiliation column should be correctly filled."
        assert df.iloc[0]["Choice Reason"] == "Professor", "The Choice Reason column should be correctly filled."
        assert df.iloc[0]["Google Scholar Home Page"] == "/citations?user=B456&hl=zh-CN&oi=sra", \
            "The Google Scholar Home Page column should be correctly filled."