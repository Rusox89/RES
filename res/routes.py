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
    report_dict = report.as_dict()
    xml = dicttoxml(report_dict)
    session.close()

    response = make_response(xml, 200)
    response.header['Content-Type'] = 'application/xml'
    return response


@res_blueprint.route('/pdf/<int:oid>', methods=['GET'])
def pdf_handler(oid):
    """
        Retrieves the object id from the path and returns the
        report in pdf format
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 24)
    pdf.cell(40, 10, 'The Report')
    pdf_bytes = pdf.output(dest='S')

    response = make_response(pdf_bytes, 200)
    response.header['Content-Type'] = 'application/pdf'
    return response
