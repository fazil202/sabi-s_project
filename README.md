# Exam Seating Plan Generator

## Abstract
The Exam Seating Plan Generator is a Python-based web application designed to automate and streamline the process of generating fair seating arrangements for examinations. It reads input data from two CSV files — one containing student details (roll number, name, branch, and section), and another describing room layouts (room number, rows, columns, and allowed branches).

The project is built using Python with the Flask web framework, and incorporates HTML and CSS for the user interface. It also uses libraries such as pandas for data manipulation for efficient student distribution, and xhtml2pdf for converting the generated seating plan into a downloadable PDF format.

### Features
- Reads student and room data from CSV files
- Generates seating plans with constraints:
  - No two students from the same branch are seated side-by-side (left or right)
  - No two students from the same branch are seated one behind another (front-back)
  - Constraints enforced globally across all rooms
- Configurable number of students per desk
- Option to include/exclude detained students
- Assign branches to specific rooms
- Displays seating plan in web interface
- Exports seating plan to PDF

### Requirements
- Python 3.13+
- Flask
- pandas
- numpy
- xhtml2pdf

### Usage
1. Upload student and room CSV files via the web interface.
2. Configure seating options as needed.
3. Generate and view the seating plan.
4. Export the seating plan to PDF.

### Project Structure
- `app.py`: Main Flask application
- `seating.py`: Seating logic and constraints
- `pdf_export.py`: PDF export functionality
- `templates/`: HTML templates
- `static/`: CSS and static files
- `requirements.txt`: Python dependencies

### Software and Hardware Requirements
- Software: Python, Flask, xhtml2pdf, HTML, CSS, JavaScript, pandas, numpy, collections (deque)
- Hardware: Any system with minimum 4GB RAM, Intel i3 or higher processor, Windows/Linux OS
