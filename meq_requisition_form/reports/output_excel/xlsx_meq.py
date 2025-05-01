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

        headers = [
            'Name', 'Date of Request', 'Requested By', 'Department', 'Contact Number', 'Employee ID',
            'Item Name', 'Item Code', 'Item Type', 'Urgency', 'Expected Monthly Equipments',
            'Quantity Required', 'Estimated Cost per Unit', 'Total Cost', 'Unit of Measure',
            'Reason for Request', 'Item Description', 'Supplementary document',
            'Status', 'HOD Comment', 'Committee Comment', 'Committee Status'
        ]
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)

        row_num = 1
        for equipment in equipment_ids:
            worksheet.write(row_num, 0, equipment.name, string_format)
            worksheet.write(row_num, 1, str(equipment.request_date), string_format)
            worksheet.write(row_num, 2, equipment.req_by.name, string_format)
            worksheet.write(row_num, 3, equipment.dept_id.name, string_format)
            worksheet.write(row_num, 4, equipment.contact, string_format)
            worksheet.write(row_num, 5, equipment.staff_id, string_format)
            worksheet.write(row_num, 6, equipment.item_name, string_format)
            worksheet.write(row_num, 7, equipment.item_code, string_format)
            worksheet.write(row_num, 8, dict(equipment._fields['item_type'].selection).get(equipment.item_type, ''),string_format)
            # worksheet.write(row_num, 9, dict(AVAILABLE_PRIORITIES).get(equipment.urgency, ''), string_format)
            worksheet.write(row_num, 10, equipment.equipment_month or 0.0, string_format)
            worksheet.write(row_num, 11, equipment.quantity or 0.0, string_format)
            worksheet.write(row_num, 12, equipment.cost or 0.0, string_format)
            worksheet.write(row_num, 13, equipment.cost_subtotal or 0.0, string_format)
            worksheet.write(row_num, 14, equipment.uom or '', string_format)
            worksheet.write(row_num, 15, equipment.reason or '', string_format)
            worksheet.write(row_num, 16, equipment.description or '', string_format)
            worksheet.write(row_num, 17, 'Yes' if equipment.attachment else 'No', string_format)
            worksheet.write(row_num, 18, dict(equipment._fields['state'].selection).get(equipment.state, ''),
                            string_format)
            worksheet.write(row_num, 19, equipment.hod_comment or '', string_format)
            worksheet.write(row_num, 20, equipment.committee_comment or '', string_format)
            worksheet.write(row_num, 21,
                            dict(equipment._fields['committee_status'].selection).get(equipment.committee_status, ''),
                            string_format)
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
