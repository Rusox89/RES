import logging
import unittest
import requests
import random
import json
import re
import zlib
from config import CURRENT_CONFIG
from res.models import Report, get_session
from dicttoxml import dicttoxml


logging.basicConfig(level=logging.DEBUG)


class TestPDF(unittest.TestCase):
    """ Test login cases """

    def setUp(self):
        self.session = requests.session()

    def _route(self, route):
        return "http://{}:{}{}".format(
            CURRENT_CONFIG.HOSTNAME,
            CURRENT_CONFIG.PORT,
            str(route)
        )


    def _flatten_keys(self, deep_dict, flattened_dict=None):

        flattened_dict = {} if flattened_dict is None else flattened_dict
        if isinstance(deep_dict, list):
            for element in deep_dict:
                flattened_dict.update(self._flatten_keys(element, flattened_dict))

        elif not isinstance(deep_dict, dict):
            try:
                flattened_dict[deep_dict] += 1
            except KeyError:
                flattened_dict[deep_dict] = 1

        else:
            for key, value in deep_dict.items():
                flattened_dict.update(self._flatten_keys(value, flattened_dict))

        return flattened_dict


    def test_pdf_stream(self):
        """ Test the xml translation of dicttoxml """
        db_session = get_session()
        report = random.choice(list(db_session.query(Report).all()))

        response = self.session.get(
            self._route("/res/pdf/{}".format(report.id)),
        )
        print(response.content)

        text = re.search(
            b"stream\n(.*)\nendstream",
            response.content, re.M|re.S
        ).groups()[0]

        content = zlib.decompress(text)

        print(content)

        words = re.findall(b"\((.*)\)", content)

        print(words)

        print(json.loads(report.type))

        expected_words = self._flatten_keys(json.loads(report.type))

        print(expected_words)

        words = '\n'.join([str(word) for word in words])

        for key in list(expected_words.keys()):
            expected_words[key] -= len(re.findall(str(key), words))

        self.assertEquals(sum(expected_words.values()), 0)

        self.assertEqual(
            response.headers['Content-Type'], 'application/pdf', response.headers
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(dicttoxml(report.type), response.text)

    def test_no_report(self):
        pass

    def test_bad_report(self):
        pass


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestPDF("test_pdf_stream"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())

