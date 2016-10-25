import os
import json
import unittest

from textwrap import dedent
import pyexcel as pe

from .fixtures import EXPECTED_RESULTS


class TestIO(unittest.TestCase):

    TABLEFMT = 'simple'
    expected_results = EXPECTED_RESULTS['simple']

    def setUp(self):
        self.testfile = 'testfile.%s' % self.TABLEFMT
        self.testfile2 = None

    def _check_test_file(self, name):
        with open(self.testfile, "r") as f:
            written_content = f.read()

        written_content = written_content.strip('\n')

        self.assertTrue(name in self.expected_results,
                        'expected result missing: %s' % written_content)

        expected = self.expected_results[name]
        self.assertEqual(written_content, expected)

    def test_no_title_multiple_sheets(self):
        adict = {
            'sheet 1': [[1, 2], [3, 4]],
            'sheet 2': [[5, 6], [7, 8]]
        }
        pe.save_book_as(bookdict=adict, dest_file_name=self.testfile,
                        dest_write_title=False)

        self._check_test_file('no_title_multiple_sheets')

    def test_dict(self):
        adict = {
            'sheet 1': [[1, 2], [3, 4]],
            'sheet 2': [[5, 6], [7, 8]]
        }
        pe.save_book_as(bookdict=adict, dest_file_name=self.testfile)

        self._check_test_file('dict')

    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        s.save_as(self.testfile)

        self._check_test_file('normal_usage')

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)

        self._check_test_file('new_normal_usage')

    def test_no_title_single_sheet(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile,
                   dest_write_title=False)

        self._check_test_file('no_title_single_sheet')

    def test_new_normal_usage_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)

        self._check_test_file('new_normal_usage_irregular_columns')

    def test_csvbook_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        self.testfile2 = "testfile.csv"
        pe.save_as(array=content, dest_file_name=self.testfile2)
        pe.save_as(file_name=self.testfile2, dest_file_name=self.testfile)

        self._check_test_file('csvbook_irregular_columns')

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        pe.save_as(array=content, name_columns_by_row=0,
                   dest_file_name=self.testfile)

        self._check_test_file('column_series')

    def test_column_series_irregular_columns(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, '']
        ]
        pe.save_as(array=content, name_columns_by_row=0,
                   dest_file_name=self.testfile)

        self._check_test_file('column_series_irregular_columns')

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        pe.save_as(array=content, name_rows_by_column=0, name_columns_by_row=0,
                   dest_file_name=self.testfile)

        self._check_test_file('data_frame')

    def test_row_series(self):
        content = [
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]

        pe.save_as(array=content, name_rows_by_column=0,
                   dest_file_name=self.testfile)

        self._check_test_file('row_series')

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if self.testfile2 and os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestRst(TestIO):

    TABLEFMT = 'rst'
    expected_results = EXPECTED_RESULTS['rst']


class TestHTML(TestIO):

    TABLEFMT = 'html'
    expected_results = EXPECTED_RESULTS['html']


class TestJSON(TestIO):

    TABLEFMT = 'json'
    expected_results = EXPECTED_RESULTS['json']

    def _check_test_file(self, name):
        with open(self.testfile, "r") as f:
            json.load(f)

        super(TestJSON, self)._check_test_file(name)


class TestStream(unittest.TestCase):
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        # note, plus the trailing '\n'
        # due to tabluate produces the extra new line
        content = dedent("""
            pyexcel sheet:
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')
        self.assertEqual(s.simple, content)

if __name__ == "__main__":
    unittest.main()
