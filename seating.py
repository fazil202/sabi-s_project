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
                    student = student_queue.popleft()
                    conflict = False
                    if prev_row and c < len(prev_row):
                        if prev_row[c]['Branch'] == student['Branch']:
                            conflict = True
                    if row_seats and row_seats[-1]['Branch'] == student['Branch']:
                        conflict = True
                    if conflict:
                        student_queue.append(student)
                        attempts += 1
                        if attempts > max_attempts:
                            print('Max attempts reached, cannot satisfy constraints.')
                            return None, 'Unable to satisfy seating constraints. Please check your data.'
                        continue
                    row_seats.append(student)
                    c += 1
                    attempts = 0
                room_seats.append(row_seats)
                prev_row = row_seats
            seating_plan.append({'room': room['room_number'], 'seats': room_seats})
        print('Seating plan generated.')
        return seating_plan, None
    except Exception as e:
        print('Error in seating logic:', str(e))
        return None, str(e)
