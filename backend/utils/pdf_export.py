from xhtml2pdf import pisa
import os

def export_to_pdf(seating_plan, filename='seating_plan.pdf', output_folder='.'):
    """
    Export seating plan to PDF
    
    Args:
        seating_plan: The seating plan data
        filename: Name of the PDF file (default: 'seating_plan.pdf')
        output_folder: Folder to save the PDF (default: current directory)
    
    Returns:
        str: Path to the generated PDF file
    """
    # Create better formatted HTML
    html = '''
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            h1 { color: #2d3a4b; text-align: center; margin-bottom: 30px; }
            h2 { color: #515ada; margin-top: 30px; margin-bottom: 15px; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 30px; }
            td { 
                border: 2px solid #ddd; 
                padding: 6px; 
                text-align: center; 
                vertical-align: middle;
                min-width: 130px;
                min-height: 70px;
            }
            .student { background-color: #f8f9fa; font-size: 9px; line-height: 1.1; }
            .empty { background-color: #e9ecef; color: #6c757d; font-size: 10px; }
            .roll { font-weight: bold; color: #2d3a4b; font-size: 10px; }
            .name { color: #495057; font-size: 9px; }
            .branch { color: #6c757d; font-size: 8px; }
        </style>
    </head>
    <body>
        <h1>Exam Seating Plan</h1>
    '''
    
    for room in seating_plan:
        html += f"<h2>Room: {room.get('name', room.get('room', 'Unknown Room'))}</h2>"
        html += "<table>"
        
        for row in room['seats']:
            html += '<tr>'
            for desk in row:
                if desk is not None:
                    # Check if desk contains multiple students (list) or single student (dict)
                    if isinstance(desk, list):
                        # Multiple students per desk
                        html += '<td class="student">'
                        for i, student in enumerate(desk):
                            if i > 0:
                                html += '<hr style="margin: 2px 0; border: 0.5px solid #ccc;">'
                            
                            roll_number = student.get('roll_number', 'N/A')
                            name = student.get('name', 'Unknown')
                            branch = student.get('branch', 'N/A')
                            
                            html += f'''
                            <div style="margin-bottom: 2px;">
                                <div class="roll">{roll_number}</div>
                                <div class="name">{name}</div>
                                <div class="branch">{branch}</div>
                            </div>
                            '''
                        html += '</td>'
                    else:
                        # Single student per desk
                        roll_number = desk.get('roll_number', 'N/A')
                        name = desk.get('name', 'Unknown')
                        branch = desk.get('branch', 'N/A')
                        
                        html += f'''
                        <td class="student">
                            <div class="roll">{roll_number}</div>
                            <div class="name">{name}</div>
                            <div class="branch">{branch}</div>
                        </td>
                        '''
                else:
                    html += '<td class="empty">Empty</td>'
            html += '</tr>'
        html += '</table>'
    
    html += '</body></html>'
    
    # Ensure output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Create full path
    pdf_path = os.path.join(output_folder, filename)
    
    # Generate PDF
    with open(pdf_path, 'wb') as f:
        pisa_status = pisa.CreatePDF(html, dest=f)
    
    if pisa_status.err:
        raise Exception(f"Error generating PDF: {pisa_status.err}")
    
    return pdf_path
