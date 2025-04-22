from ast import literal_eval

from odoo import http
from odoo.http import request
import io
import xlsxwriter


class XlsxPropertyReport(http.Controller):

    @http.route('/equipment/excel/report/<path:equipment_ids>', type='http', auth='user')
    def download_property_excel_report(self, equipment_ids):

        equipment_ids = request.env['meq.request'].browse(literal_eval(equipment_ids))
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Equipments')

        header_format = workbook.add_format({'bold': True,'bg_color':'#D3D3D3','border':1,'align':'center'})
        string_format = workbook.add_format({'border':1,'align':'center'})
        # price_format = workbook.add_format({'num_format':'$##,##00.00','border':1,'align':'center'})

        headers = ['Name','Request Date']
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for equipment in equipment_ids:
            worksheet.write(row_num, 0, equipment.name, string_format)
            worksheet.write(row_num, 1, equipment.request_date, string_format)
            # worksheet.write(row_num, 1, 'Yes' if property.color else 'No', string_format)
            row_num += 1

        workbook.close()
        output.seek(0)

        file_name = 'Equipment Report.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename= {file_name}')
            ]
        )
