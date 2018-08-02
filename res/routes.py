from flask import Blueprint, make_response
from res.models import Report, get_session
from dicttoxml import dicttoxml
from fpdf import FPDF

res_blueprint = Blueprint('res', __name__, url_prefix='/res')


@res_blueprint.route('/xml/<int:oid>', methods=['GET'])
def xml_handler(oid):
    """
        Retrieves the object id from the path and returns the
        report in xml format
    """
    session = get_session()
    report = session.query(Report).get(oid)
    report_dict = report.to_dict()
    xml = dicttoxml(report_dict)
    session.close()

    response = make_response(xml, 200)
    response.headers['Content-Type'] = 'application/xml'
    return response


@res_blueprint.route('/pdf/<int:oid>', methods=['GET'])
def pdf_handler(oid):
    """
        Retrieves the object id from the path and returns the
        report in pdf format
    """
    session = get_session()
    report = session.query(Report).get(oid)
    report_dict = report.to_dict()
    session.close()

    # Create PDF object
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set title
    pdf.set_title("THE REPORT")

    # Print title
    pdf.set_font('Arial', 'B', 24)
    pdf.set_xy(75, 30)
    pdf.cell(0, 0, "THE REPORT")

    # Print right box
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(120, 50)
    pdf.multi_cell(
        0, 3,
        "\n".join(
            [
                "Organization: {}\n".format(report_dict['organization']),
                "Reported: {}\n".format(report_dict['reported_at']),
                "Created: {}".format(report_dict['created_at'])
            ]
        )
    )

    # Print report inventory
    pdf.set_font('Arial', 'B', 12)
    pdf.set_xy(75, 150)
    inventory_text = '\n'.join(
        [
            "{price:_<10} {name}".format(**element)
            for element in report_dict['inventory']
        ]
    )
    pdf.multi_cell(0, 5, inventory_text)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')

    response = make_response(pdf_bytes, 200)
    response.headers['Content-Type'] = 'application/pdf'
    return response
