#!/usr/bin/env python3

"""UNC to URL Converter tests."""

import io
import sys
import unittest
import unittest.mock

# import unc2url
from unc2url import unc2url


class UNCTestCase(unittest.TestCase):
    """UNC to URL Converter tests."""

    UNC = "\\\\example.org\\acme\\data\\Regelmäßige Meetings\\path"
    URL = "smb://example.org/acme/data/Regelmäßige%20Meetings/path"
    FILE = "file://example.org/acme/data/Regelmäßige%20Meetings/path"

    def test_main(self):
        with self.assertRaises(SystemExit):
            unc2url.main()
        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as fake_out:
            sys.argv = ["", self.UNC]
            unc2url.main()
            self.assertEqual(fake_out.getvalue().strip(), self.URL)
        with unittest.mock.patch("sys.stdout", new=io.StringIO()) as fake_out:
            sys.argv = ["", "-r", self.URL]
            unc2url.main()
            self.assertEqual(fake_out.getvalue().strip(), self.UNC)

    def test_unc_to_url(self):
        result = unc2url.unc_to_url(" " + self.UNC + "\n")
        self.assertEqual(self.URL, result)

    def test_unc_to_file(self):
        result = unc2url.unc_to_url(self.UNC, True)
        self.assertEqual(self.FILE, result)

    def test_url_to_unc(self):
        result = unc2url.url_to_unc(self.URL + " ")
        self.assertEqual(self.UNC, result)

    def test_file_to_unc(self):
        result = unc2url.url_to_unc(self.FILE)
        self.assertEqual(self.UNC, result)


if __name__ == "__main__":
    unittest.main()
