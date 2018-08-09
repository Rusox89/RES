from unittest import TextTestRunner, TestSuite
from test_xml import suite as xml_suite
from pdf_entries import suite as pdf_suite

if __name__ == "__main__":
    test_suites = [
        auth_suite,
        entry_suite
    ]
    main_suite = TestSuite()
    for suite in test_suites:
        main_suite.addTests(suite())
    ttr = TextTestRunner()
    ttr.run(main_suite)
