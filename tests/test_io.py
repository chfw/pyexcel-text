import os
import sys
import json
import unittest

from textwrap import dedent
import pyexcel as pe
from pyexcel.ext import text
if sys.version_info[0] < 3:
    from StringIO import StringIO
else:
    from io import StringIO

# Python 2.6 does not have unittest.expectedFailure; just ignore those test
if hasattr(unittest, 'expectedFailure'):
    expectedFailure = unittest.expectedFailure
else:
    expectedFailure = lambda func: lambda x: 'skip'

class TestIO(unittest.TestCase):

    TABLEFMT = 'simple'
    expected_results = {
        'dict': dedent("""
            Sheet Name: sheet 1
            -  -
            1  2
            3  4
            -  -
            Sheet Name: sheet 2
            -  -
            5  6
            7  8
            -  -""").strip('\n'),
    }

    def setUp(self):
        text.TABLEFMT = self.TABLEFMT
        self.testfile = 'testfile.%s' % self.TABLEFMT
        self.testfile2 = None

    def _check_test_file(self, name):
        with open(self.testfile, "r") as f:
            written_content = f.read()

        written_content = written_content.strip('\n')

        self.assertTrue(name in self.expected_results)

        expected = self.expected_results[name]

        self.assertEqual(written_content, expected)

    def test_dict(self):
        adict = {
            'sheet 1': [[1,2],[3,4]],
            'sheet 2': [[5,6],[7,8]]
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
        text.save_as(s, self.testfile)

        self._check_test_file('normal_usage')

    expected_results['normal_usage'] = dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')

    def test_new_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)

        self._check_test_file('new_normal_usage')

    expected_results['new_normal_usage'] = dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')

    def test_new_normal_usage_irregular_columns(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8]
        ]
        pe.save_as(array=content, dest_file_name=self.testfile)

        self._check_test_file('new_normal_usage_irregular_columns')

    expected_results['new_normal_usage_irregular_columns'] = dedent("""
            Sheet Name: pyexcel_sheet1
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n')

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

    expected_results['csvbook_irregular_columns'] = dedent("""
            Sheet Name: testfile.csv
            -  ---  -
            1    2  3
            4  588  6
            7    8
            -  ---  -""").strip('\n')

    def test_column_series(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]
        ]
        s = pe.Sheet(content, name_columns_by_row=0)

        pe.save_as(array=s, dest_file_name=self.testfile)

        self._check_test_file('column_series')

    expected_results['column_series'] = dedent("""
            Sheet Name: pyexcel_sheet1
              Column 1    Column 2    Column 3
            ----------  ----------  ----------
                     1           2           3
                     4           5           6
                     7           8           9""").strip('\n')

    def test_column_series_irregular_columns(self):
        content = [
            ["Column 1", "Column 2", "Column 3"],
            [1, 2, 3],
            [4, 5, 6],
            [7, 8]
        ]
        s = pe.Sheet(content, name_columns_by_row=0)

        pe.save_as(array=s, dest_file_name=self.testfile)

        self._check_test_file('column_series_irregular_columns')

        # FIXME: numerical align lost when one cell is missing
    expected_results['column_series_irregular_columns'] = dedent("""
            Sheet Name: pyexcel_sheet1
              Column 1    Column 2  Column 3
            ----------  ----------  ----------
                     1           2  3
                     4           5  6
                     7           8""").strip('\n')

    def test_data_frame(self):
        content = [
            ["", "Column 1", "Column 2", "Column 3"],
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0, name_columns_by_row=0)

        pe.save_as(array=s, dest_file_name=self.testfile)

        self._check_test_file('data_frame')

    expected_results['data_frame'] = dedent("""
            Sheet Name: pyexcel_sheet1
                     Column 1    Column 2    Column 3
            -----  ----------  ----------  ----------
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9""").strip('\n')

    def test_row_series(self):
        content = [
            ["Row 1", 1, 2, 3],
            ["Row 2", 4, 5, 6],
            ["Row 3", 7, 8, 9]
        ]
        s = pe.Sheet(content, name_rows_by_column=0)

        pe.save_as(array=s, dest_file_name=self.testfile)

        self._check_test_file('row_series')

    expected_results['row_series'] = dedent("""
            Sheet Name: pyexcel_sheet1
            -----  -  -  -
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            -----  -  -  -""").strip('\n')

    def tearDown(self):
        if os.path.exists(self.testfile):
            os.unlink(self.testfile)
        if self.testfile2 and os.path.exists(self.testfile2):
            os.unlink(self.testfile2)


class TestRst(TestIO):

    TABLEFMT = 'rst'
    expected_results = {
        'normal_usage': dedent("""
            Sheet Name: pyexcel
            =  ===  ===
            1    2    3
            4  588    6
            7    8  999
            =  ===  ===""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'column_series': dedent("""
            Sheet Name: pyexcel_sheet1
            ==========  ==========  ==========
              Column 1    Column 2    Column 3
            ==========  ==========  ==========
                     1           2           3
                     4           5           6
                     7           8           9
            ==========  ==========  ==========""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            Sheet Name: pyexcel_sheet1
            ==========  ==========  ==========
              Column 1    Column 2  Column 3
            ==========  ==========  ==========
                     1           2  3
                     4           5  6
                     7           8
            ==========  ==========  ==========""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            Sheet Name: testfile.csv
            =  ===  =
            1    2  3
            4  588  6
            7    8
            =  ===  =""").strip('\n'),
        'data_frame': dedent("""
            Sheet Name: pyexcel_sheet1
            =====  ==========  ==========  ==========
                     Column 1    Column 2    Column 3
            =====  ==========  ==========  ==========
            Row 1           1           2           3
            Row 2           4           5           6
            Row 3           7           8           9
            =====  ==========  ==========  ==========""").strip('\n'),
        'row_series': dedent("""
            Sheet Name: pyexcel_sheet1
            =====  =  =  =
            Row 1  1  2  3
            Row 2  4  5  6
            Row 3  7  8  9
            =====  =  =  =""").strip('\n'),

    }

    expected_results['new_normal_usage'] = dedent("""
        Sheet Name: pyexcel_sheet1
        =  ===  ===
        1    2    3
        4  588    6
        7    8  999
        =  ===  ===""").strip('\n')

    expected_results['dict'] = dedent("""
        Sheet Name: sheet 1
        =  =
        1  2
        3  4
        =  =
        Sheet Name: sheet 2
        =  =
        5  6
        7  8
        =  =""").strip('\n')


class TestHTML(TestIO):

    TABLEFMT = 'html'
    expected_results = {
        'dict': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: sheet 1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">2</td></tr>
            <tr><td style="text-align: right;">3</td><td style="text-align: right;">4</td></tr>
            </table>
            Sheet Name: sheet 2
            <table>
            <tr><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">8</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'normal_usage': dedent("""
            Sheet Name: pyexcel
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>""").strip('\n'),
        'new_normal_usage': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td style="text-align: right;">  3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td style="text-align: right;">  6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td style="text-align: right;">999</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'new_normal_usage_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'column_series': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'column_series_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th>Column 3  </th></tr>
            <tr><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td>3         </td></tr>
            <tr><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td>6         </td></tr>
            <tr><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td>          </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'csvbook_irregular_columns': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: testfile.csv
            <table>
            <tr><td style="text-align: right;">1</td><td style="text-align: right;">  2</td><td>3</td></tr>
            <tr><td style="text-align: right;">4</td><td style="text-align: right;">588</td><td>6</td></tr>
            <tr><td style="text-align: right;">7</td><td style="text-align: right;">  8</td><td> </td></tr>
            </table>
            </body></html>""").strip('\n'),
        'data_frame': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><th>     </th><th style="text-align: right;">  Column 1</th><th style="text-align: right;">  Column 2</th><th style="text-align: right;">  Column 3</th></tr>
            <tr><td>Row 1</td><td style="text-align: right;">         1</td><td style="text-align: right;">         2</td><td style="text-align: right;">         3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">         4</td><td style="text-align: right;">         5</td><td style="text-align: right;">         6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">         7</td><td style="text-align: right;">         8</td><td style="text-align: right;">         9</td></tr>
            </table>
            </body></html>""").strip('\n'),
        'row_series': dedent("""
            <html><header><title>testfile.html</title><body>Sheet Name: pyexcel_sheet1
            <table>
            <tr><td>Row 1</td><td style="text-align: right;">1</td><td style="text-align: right;">2</td><td style="text-align: right;">3</td></tr>
            <tr><td>Row 2</td><td style="text-align: right;">4</td><td style="text-align: right;">5</td><td style="text-align: right;">6</td></tr>
            <tr><td>Row 3</td><td style="text-align: right;">7</td><td style="text-align: right;">8</td><td style="text-align: right;">9</td></tr>
            </table>
            </body></html>
            """).strip('\n'),
    }


class TestJSON(TestIO):

    TABLEFMT = 'json'
    expected_results = {
        'dict':
            '{"sheet 1": [[1, 2], [3, 4]], "sheet 2": [[5, 6], [7, 8]]}',
        'normal_usage':
            '{"pyexcel": [[1, 2, 3], [4, 588, 6], [7, 8, 999]]}',
        'new_normal_usage':
            '[[1, 2, 3], [4, 588, 6], [7, 8, 999]]',
        'new_normal_usage_irregular_columns':
            '[[1, 2, 3], [4, 588, 6], [7, 8]]',
    }

    def _check_test_file(self, name):
        with open(self.testfile, "r") as f:
            json.load(f)

        super(TestJSON, self)._check_test_file(name)

    # These all raise TypeError: x is not JSON serializable
    @expectedFailure
    def test_column_series(self):
        super(TestJSON, self).test_column_series()

    @expectedFailure
    def test_column_series_irregular_columns(self):
        super(TestJSON, self).test_column_series_irregular_columns()

    @expectedFailure
    def test_csvbook_irregular_columns(self):
        super(TestJSON, self).test_csvbook_irregular_columns()

    @expectedFailure
    def test_row_series(self):
        super(TestJSON, self).test_row_series()

    @expectedFailure
    def test_data_frame(self):
        super(TestJSON, self).test_data_frame()


class TestStream:
    def setUp(self):
        self.testfile = StringIO()
        text.TABLEFMT = "simple"
    def test_normal_usage(self):
        content = [
            [1, 2, 3],
            [4, 588, 6],
            [7, 8, 999]
        ]
        s = pe.Sheet(content)
        text.save_to_memory(s, self.testfile)
        written_content = self.testfile.getvalue()
        content = dedent("""
            Sheet Name: pyexcel
            -  ---  ---
            1    2    3
            4  588    6
            7    8  999
            -  ---  ---""").strip('\n')
        assert written_content == content

if __name__ == "__main__":
    unittest.main()
