from xhtml2pdf import pisa
import os

def export_to_pdf(seating_plan):
    html = '<html><body><h1>Seating Plan</h1>'
    for room in seating_plan:
        html += f"<h2>Room {room['room']}</h2><table border='1'>"
        for row in room['seats']:
            html += '<tr>'
            for student in row:
                if student is not None:
                    html += f"<td>{student['roll_number']}<br>{student['name']}<br>{student['branch']}</td>"
                else:
                    html += '<td>Empty</td>'
            html += '</tr>'
        html += '</table>'
    html += '</body></html>'
    pdf_path = os.path.join('static', 'seating_plan.pdf')
    with open(pdf_path, 'wb') as f:
        pisa.CreatePDF(html, dest=f)
    return pdf_path
