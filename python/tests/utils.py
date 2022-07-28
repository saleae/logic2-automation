import filecmp
import difflib


def assert_files_match(expected, actual, binary=False):
    if binary:
        assert filecmp.cmp(expected, actual)
    else:
        if filecmp.cmp(expected, actual):
            assert True
            return

        with open(expected) as f:
            expected_data = f.readlines()

        with open(actual) as f:
            actual_data = f.readlines()

        diff = difflib.unified_diff(expected_data, actual_data, fromfile=expected, tofile=actual)
        diffstr = ''.join(diff)

        assert diffstr == '', f'Files ${expected} and ${actual} do not match: ${diffstr}'
