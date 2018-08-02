""" Helpers module """
from fpdf import FPDF


class PDFReport(FPDF):
    """ Class representing a PDF Report """

    # Required by python3 and fpdf
    ENCODING = 'latin-1'

    FAMILY = 'Arial'

    def __init__(self, abstract_report, *args, **kwargs):
        super(PDFReport, self).__init__(*args, **kwargs)
        self.add_page()
        self.set_title("THE REPORT")
        self.print_title("The Report")
        self.print_info(
            abstract_report['organization'],
            abstract_report['reported_at'],
            abstract_report['created_at']
        )
        self.print_inventory(
            abstract_report['inventory']
        )

    def print_title(self, title):
        """ Prints the title """
        self.set_font(self.FAMILY, 'B', 24)
        self.set_xy(75, 30)
        self.cell(0, 0, title)

    def print_info(self, organization, reported_at, created_at):
        """ Prints the organizational information """
        self.set_font(self.FAMILY, 'B', 12)
        self.set_xy(120, 50)
        self.multi_cell(
            0, 3,
            "\n".join(
                [
                    "Organization: {}\n".format(organization),
                    "Reported: {}\n".format(reported_at),
                    "Created: {}".format(created_at)
                ]
            )
        )

    def print_inventory(self, inventory):
        """ Prints the inventory """
        self.set_font(self.FAMILY, 'B', 12)
        self.set_xy(75, 150)
        inventory_text = '\n'.join(
            [
                "{price:_<10} {name}".format(**element)
                for element in inventory
            ]
        )
        self.multi_cell(0, 5, inventory_text)

    def bytes(self):
        return self.output(dest='S').encode(self.ENCODING)
