from odoo import api, fields, models
import base64


class hr_salary_employee_bymonth(models.TransientModel):

    _name = 'hr.salary.employee.month'
    _description = 'Libro de Remuneraciones Haberes'

    def _get_default_end_date(self):
        date = fields.Date.from_string(fields.Date.today())
        return date.strftime('%Y') + '-' + date.strftime('%m') + '-' + date.strftime('%d')

    end_date = fields.Date(string='End Date', required=True, default=_get_default_end_date)

    def library(self):
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        date = data['form']['end_date'].strftime('%Y-%m-%d')
        data['form']['end_date'] = date
        get_employee2 = self.env['report.l10n_cl_hr.report_hrsalarybymonth'].get_employee2(data['form'])
        file_name = 'libro de remuneraciones.txt'
        lines = []
        for emp in get_employee2:
            library = ''
            name = ''
            if emp[2]:
                name += emp[2]
            if emp[3]:
                name += ' ' + emp[3]
            if emp[4]:
                name += ' ' + emp[4]
            if emp[5]:
                name += ' ' + emp[5]  
            library += str(emp[0])+ ',' if emp[0] else ''
            library+=str(emp[1])+ ','
            library+=str(name)+ ','
            library+=str(emp[6])+ ',' 
            library+=str(emp[7])+ ',' 
            library+=str(emp[8])+ ',' 
            library+=str(emp[9])+ ',' 
            library+=str(emp[11])+ ',' 
            library+=str(emp[12])+ ',' 
            library+=str(emp[13])+ ',' 
            library+=str(emp[14])+ ',' 
            library+=str(emp[15])
            lines.append(library)
       
        output = ''
        for line in lines:
            output += line + '\n'

        data = base64.encodebytes(output.encode()),

        doc = self.env['ir.attachment'].create({
            'name': '%s' % (file_name),
            'datas': data[0],
            'store_fname': '%s' % (file_name),
            'type': 'binary'
        })
           
        return {
            'type': "ir.actions.act_url",
            'url': "web/content/?model=ir.attachment&id=" + str(
                doc.id) + "&filename_field=name&field=datas&download=true&filename=" + str(doc.name),
            'target': "self",
            'no_destroy': False,
        }
    
        


    def print_report(self):
        """
         To get the date and print the report
         @return: return report
        """
        self.ensure_one()
        data = {'ids': self.env.context.get('active_ids', [])}
        res = self.read()
        res = res and res[0] or {}
        data.update({'form': res})
        return self.env.ref('l10n_cl_hr.hr_salary_books').report_action(self, data=data)
