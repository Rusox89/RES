import logging
import unittest
import requests
import random
import json
from config import CURRENT_CONFIG
from res.models import Report, get_session
from dicttoxml import dicttoxml


logging.basicConfig(level=logging.DEBUG)


class TestXML(unittest.TestCase):
    """ Test login cases """

    def setUp(self):
        self.session = requests.session()
        self.session.headers['Content-Type'] = 'application/json'

    def _route(self, route):
        return "http://{}:{}{}".format(
            CURRENT_CONFIG.HOSTNAME,
            CURRENT_CONFIG.PORT,
            str(route)
        )

    def test_xml_report_via_dicttoxml(self):
        """ Test the xml translation of dicttoxml """
        db_session = get_session()
        report = random.choice(list(db_session.query(Report).all()))

        response = self.session.get(
            self._route("/res/xml/{}".format(report.id)),
        )

        self.assertEqual(
            response.headers['Content-Type'], 'application/xml', response.headers
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(dicttoxml(report.description), response.text)

    def test_no_report(self):
        pass

    def test_bad_report(self):
        pass

    def test_xml_report_via_structure_navigation(self):
        """ Test the xml translation of dicttoxml """
        db_session = get_session()
        report = random.choice(list(db_session.query(Report).all()))
        expected = json.loads(report.description)
        response = self.session.get(
            self._route("/res/xml/{}".format(report.id)),
        )

        self.assertEqual(
            response.headers['Content-Type'], 'application/xml', response.headers
        )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertTrue(self._xml_equals_dict(expected, response))

    def _xml_equals_dict(self, expected, response):
        for dict_key, dict_value in expected.items():
            if isinstance(dict_value, list) or isinstance(dict_value, dict):
                self._xml_equals_dict(dict_value, response)


def suite():
    suite = unittest.TestSuite()
    suite.addTest(TestXML("test_post_successful_login"))
    suite.addTest(TestXML("test_logout"))
    suite.addTest(TestXML("test_logout_without_login"))
    suite.addTest(TestXML("test_post_successful_login"))
    suite.addTest(TestXML("test_post_unsuccessful_credentials"))
    suite.addTest(TestXML("test_post_wrong_type_credentials"))
    suite.addTest(TestXML("test_post_malformed"))
    suite.addTest(TestXML("test_put"))
    suite.addTest(TestXML("test_delete"))
    suite.addTest(TestXML("test_get"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())

