import pandas as pd
import numpy as np
from collections import deque

def generate_seating_plan(student_csv, room_csv, students_per_desk, include_detained):
    try:
        print('Reading student CSV:', student_csv)
        students = pd.read_csv(student_csv)
        print('Student data loaded:', students.shape)
        rooms = pd.read_csv(room_csv)
        print('Room data loaded:', rooms.shape)
        detained_col = None
        for col in ['detained', 'detained_status']:
            if col in students.columns:
                detained_col = col
                break
        if not include_detained and detained_col:
            students = students[students[detained_col] == False]
            print(f"Filtered detained students using column '{detained_col}':", students.shape)
        elif not include_detained:
            print("Warning: 'detained' or 'detained_status' column not found in student CSV. Skipping filter.")
        grouped = students.groupby(['Branch', 'Section'])
        student_queue = deque()
        for _, group in grouped:
            for _, row in group.iterrows():
                student_queue.append(row)
        print('Student queue length:', len(student_queue))
        seating_plan = []
        prev_row = []
        max_attempts = len(student_queue) * 2  # Prevent infinite loop
        for _, room in rooms.iterrows():
            print('Processing room:', room['room_number'])
            room_seats = []
            for r in range(room['rows']):
                print('Processing row:', r)
                row_seats = []
                c = 0
                attempts = 0
                while c < room['columns']:
                    if not student_queue:
                        row_seats.append(None)
                        c += 1
                        continue
                    
                    # Handle multiple students per desk
                    desk_students = []
                    students_placed = 0
                    desk_attempts = 0
                    
                    while students_placed < students_per_desk and student_queue and desk_attempts < max_attempts:
                        student = student_queue.popleft()
                        conflict = False
                        
                        # Convert pandas row to dictionary for easier handling
                        student_dict = {
                            'roll_number': student.get('Roll Number', student.get('roll_number', 'N/A')),
                            'name': student.get('Name', student.get('name', 'Unknown')),
                            'branch': student.get('Branch', student.get('branch', 'N/A'))
                        }
                        
                        # Check for conflicts with students already in this desk
                        for desk_student in desk_students:
                            if desk_student['branch'] == student_dict['branch']:
                                conflict = True
                                break
                        
                        # Check for conflicts with previous row
                        if not conflict and prev_row and c < len(prev_row) and prev_row[c] is not None:
                            if isinstance(prev_row[c], list):
                                for prev_student in prev_row[c]:
                                    if prev_student and prev_student['branch'] == student_dict['branch']:
                                        conflict = True
                                        break
                            elif prev_row[c]['branch'] == student_dict['branch']:
                                conflict = True
                        
                        # Check for conflicts with adjacent desk in same row
                        if not conflict and row_seats and row_seats[-1] is not None:
                            if isinstance(row_seats[-1], list):
                                for adj_student in row_seats[-1]:
                                    if adj_student and adj_student['branch'] == student_dict['branch']:
                                        conflict = True
                                        break
                            elif row_seats[-1]['branch'] == student_dict['branch']:
                                conflict = True
                        
                        if conflict:
                            student_queue.append(student)
                            desk_attempts += 1
                            continue
                            
                        desk_students.append(student_dict)
                        students_placed += 1
                        desk_attempts = 0
                    
                    # If we couldn't place any students due to conflicts, break the loop
                    if students_placed == 0 and desk_attempts >= max_attempts:
                        print('Max attempts reached, cannot satisfy constraints.')
                        return None, [], 'Unable to satisfy seating constraints. Please check your data.'
                    
                    # Store the desk (single student or list of students)
                    if students_per_desk == 1:
                        row_seats.append(desk_students[0] if desk_students else None)
                    else:
                        row_seats.append(desk_students if desk_students else None)
                    
                    c += 1
                    attempts = 0
                room_seats.append(row_seats)
                prev_row = row_seats
            seating_plan.append({'room': room['room_number'], 'seats': room_seats})
        # Collect unseated students
        unseated_students = []
        while student_queue:
            student = student_queue.popleft()
            unseated_students.append({
                'roll_number': student.get('Roll Number', student.get('roll_number', 'N/A')),
                'name': student.get('Name', student.get('name', 'Unknown')),
                'branch': student.get('Branch', student.get('branch', 'N/A'))
            })
        
        print('Seating plan generated.')
        print(f'Unseated students: {len(unseated_students)}')
        return seating_plan, unseated_students, None
    except Exception as e:
        print('Error in seating logic:', str(e))
        return None, [], str(e)
