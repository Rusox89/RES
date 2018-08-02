from flask import Blueprint, make_response, abort
from res.models import Report, get_session
from dicttoxml import dicttoxml
from res.helpers import PDFReport

res_blueprint = Blueprint('res', __name__, url_prefix='/res')


@res_blueprint.route('/xml/<int:oid>', methods=['GET'])
def xml_handler(oid):
    """
        Retrieves the object id from the path and returns the
        report in xml format
    """
    session = get_session()
    report = session.query(Report).get(oid)
    if report is None:
        abort(404)
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
    if report is None:
        abort(404)
    report_dict = report.to_dict()
    session.close()

    # Create PDF object
    pdf = PDFReport(report_dict)
    pdf_bytes = pdf.bytes()

    response = make_response(pdf_bytes, 200)
    response.headers['Content-Type'] = 'application/pdf'
    return response
