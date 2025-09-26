import pandas as pd
import math
from collections import deque

def generate_seating_plan(student_csv_path, room_csv_path, students_per_desk=1, include_detained=False):
    """
    Generate seating plan based on CSV files
    """
    try:
        # Read CSV files
        students_df = pd.read_csv(student_csv_path)
        rooms_df = pd.read_csv(room_csv_path)
        
        # Debug: Print column names and data types
        print(f"Students CSV columns: {list(students_df.columns)}")
        print(f"Rooms CSV columns: {list(rooms_df.columns)}")
        print(f"Include detained setting: {include_detained}")
        print(f"Room data sample:\n{rooms_df.head()}")
        
        # Normalize column names (handle case variations)
        students_df.columns = students_df.columns.str.lower().str.strip()
        rooms_df.columns = rooms_df.columns.str.lower().str.strip()
        
        print(f"Normalized room columns: {list(rooms_df.columns)}")
        print(f"Room DataFrame after normalization:\n{rooms_df}")
        
        # Handle different column name variations for detained status
        detained_column = None
        for col in students_df.columns:
            if 'detained' in col.lower():
                detained_column = col
                break
        
        if detained_column:
            print(f"Found detained column: {detained_column}")
            print(f"Detained status values: {students_df[detained_column].value_counts()}")
        
        # Filter students based on include_detained setting
        if include_detained:
            filtered_students = students_df.copy()
            print(f"Including ALL students: {len(filtered_students)} total")
        else:
            if detained_column:
                detained_mask = students_df[detained_column].astype(str).str.upper().isin(['TRUE', '1', 'YES', 'Y'])
                filtered_students = students_df[~detained_mask]
                print(f"Excluding detained students: {len(filtered_students)} non-detained out of {len(students_df)} total")
            else:
                filtered_students = students_df.copy()
                print(f"No detained column found, including all {len(filtered_students)} students")
        
        print(f"Final student count for seating: {len(filtered_students)}")
        
        if len(filtered_students) == 0:
            return [], [], "No students available for seating arrangement."
        
        # Prepare student list
        students = []
        for _, student in filtered_students.iterrows():
            student_info = {
                'roll_number': student.get('roll_number', student.get('id', 'N/A')),
                'name': student.get('name', 'Unknown'),
                'branch': student.get('branch', student.get('department', 'N/A')),
                'section': student.get('section', 'N/A'),
                'detained': False if not detained_column else 
                           str(student.get(detained_column, 'FALSE')).upper() in ['TRUE', '1', 'YES', 'Y']
            }
            students.append(student_info)
        
        # Debug: Show sample students
        print(f"Sample students (first 3): {students[:3]}")
        
        # Prepare room list with enhanced debugging
        rooms = []
        print("\n=== ROOM PROCESSING DEBUG ===")
        
        for idx, room in rooms_df.iterrows():
            print(f"\nProcessing room index {idx}:")
            print(f"Raw room data: {dict(room)}")
            
            # Handle multiple possible column names for room identification
            room_number = None
            room_name = None
            capacity = None
            
            # Try different column names for room number/name
            room_columns = ['room_number', 'room_name', 'room', 'name', 'room_id', 'room_no']
            for col in room_columns:
                if col in rooms_df.columns and pd.notna(room.get(col)):
                    if room_number is None:
                        room_number = str(room.get(col)).strip()
                    if 'name' in col.lower() and room_name is None:
                        room_name = str(room.get(col)).strip()
                    print(f"Found {col}: '{room.get(col)}'")
            
            # If no specific room_name found, use room_number
            if room_name is None:
                room_name = room_number
            
            # Try different column names for capacity
            capacity_columns = ['capacity', 'seats', 'max_seats', 'total_seats']
            for col in capacity_columns:
                if col in rooms_df.columns and pd.notna(room.get(col)):
                    try:
                        capacity = int(float(room.get(col)))
                        print(f"Found capacity in {col}: {capacity}")
                        break
                    except (ValueError, TypeError):
                        continue
            
            # Default values if not found
            if room_number is None:
                room_number = f'Room_{idx + 1}'
                print(f"Using default room_number: {room_number}")
            
            if room_name is None:
                room_name = room_number
                print(f"Using room_number as room_name: {room_name}")
                
            if capacity is None:
                capacity = 30
                print(f"Using default capacity: {capacity}")
            
            room_info = {
                'room_number': room_number,
                'room_name': room_name,
                'capacity': capacity,
                'building': str(room.get('building', 'Main Building')),
                'floor': str(room.get('floor', '1'))
            }
            
            print(f"Final room_info: {room_info}")
            rooms.append(room_info)
        
        print(f"\n=== FINAL ROOMS LIST ===")
        for i, r in enumerate(rooms):
            print(f"Room {i+1}: number='{r['room_number']}', name='{r['room_name']}', capacity={r['capacity']}")
        
        # Sort rooms by room number for consistent allocation
        rooms.sort(key=lambda x: str(x['room_number']))
        
        # Generate seating arrangement
        seating_plan = []
        student_queue = deque(students)
        unseated_students = []
        total_seated = 0
        
        for room in rooms:
            if not student_queue:
                break
                
            room_capacity = room['capacity']
            seats_per_row = 6
            rows = math.ceil(room_capacity / seats_per_row)
            
            room_seating = {
                'room_number': room['room_number'],
                'room_name': room['room_name'],
                'building': room['building'],
                'floor': room['floor'],
                'capacity': room_capacity,
                'seats': [],
                'students_count': 0
            }
            
            # Create seating arrangement for this room
            seats_filled = 0
            room_student_count = 0
            
            for row_num in range(rows):
                row = []
                for seat_num in range(seats_per_row):
                    if seats_filled >= room_capacity or not student_queue:
                        row.append(None)
                    else:
                        seat_students = []
                        for _ in range(students_per_desk):
                            if student_queue and seats_filled < room_capacity:
                                student = student_queue.popleft()
                                seat_students.append(student)
                                total_seated += 1
                                room_student_count += 1
                                seats_filled += 1
                        
                        if seat_students:
                            row.append(seat_students)
                        else:
                            row.append(None)
                
                room_seating['seats'].append(row)
            
            room_seating['students_count'] = room_student_count
            seating_plan.append(room_seating)
            
            print(f"Added to seating plan - Room '{room['room_name']}' ({room['room_number']}): {room_student_count} students")
        
        unseated_students = list(student_queue)
        
        print(f"\n=== SEATING PLAN SUMMARY ===")
        print(f"Total students seated: {total_seated}")
        print(f"Total unseated students: {len(unseated_students)}")
        print(f"Total rooms used: {len(seating_plan)}")
        
        for i, room in enumerate(seating_plan):
            print(f"Plan Room {i+1}: '{room['room_name']}' - {room['students_count']} students")
        
        return seating_plan, unseated_students, None
        
    except Exception as e:
        error_msg = f"Error generating seating plan: {str(e)}"
        print(error_msg)
        import traceback
        traceback.print_exc()
        return [], [], error_msg

def validate_csv_format(csv_path, expected_type):
    """
    Validate CSV file format
    """
    try:
        df = pd.read_csv(csv_path)
        
        if expected_type == 'students':
            required_columns = ['name']
            optional_columns = ['roll_number', 'id', 'branch', 'department', 'section', 'detained_status', 'detained']
        elif expected_type == 'rooms':
            required_columns = ['room_number', 'room_name', 'room', 'capacity', 'seats']
            optional_columns = ['building', 'floor']
        else:
            return False, "Unknown CSV type"
        
        df_columns_normalized = [col.lower().strip() for col in df.columns]
        required_normalized = [col.lower() for col in required_columns]
        
        found_required = any(req in df_columns_normalized for req in required_normalized)
        
        if not found_required:
            return False, f"Missing required columns. Expected one of: {required_columns}"
        
        return True, "Valid format"
        
    except Exception as e:
        return False, f"Error reading CSV: {str(e)}"

def get_room_summary(seating_plan):
    """
    Generate summary of room allocation
    """
    summary = []
    total_students = 0
    
    for room in seating_plan:
        room_students = room.get('students_count', 0)
        total_students += room_students
        
        summary.append({
            'room_number': room.get('room_number', 'Unknown'),
            'room_name': room.get('room_name', room.get('room_number', 'Unknown')),
            'capacity': room.get('capacity', 0),
            'students_seated': room_students,
            'utilization': f"{(room_students/room.get('capacity', 1)*100):.1f}%" if room.get('capacity', 0) > 0 else "0%"
        })
    
    return summary, total_students
