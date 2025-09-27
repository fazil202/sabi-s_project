import pandas as pd
import math
import random
from collections import deque, defaultdict

def generate_seating_plan(student_csv_path, room_csv_path, students_per_desk=1, include_detained=False):
    """
    Generate seating plan ensuring no same-branch students sit left-right or front-back
    """
    try:
        # Read CSVs
        students_df = pd.read_csv(student_csv_path)
        rooms_df = pd.read_csv(room_csv_path)

        # Normalize columns
        students_df.columns = students_df.columns.str.lower().str.strip()
        rooms_df.columns = rooms_df.columns.str.lower().str.strip()

        # Detect detained column
        detained_column = None
        for col in students_df.columns:
            if 'detained' in col.lower():
                detained_column = col
                break

        # Filter detained students if needed
        if include_detained or not detained_column:
            filtered_students = students_df.copy()
        else:
            detained_mask = students_df[detained_column].astype(str).str.upper().isin(['TRUE', '1', 'YES', 'Y'])
            filtered_students = students_df[~detained_mask]

        if len(filtered_students) == 0:
            return [], [], "No students available for seating."

        # Group by branch
        students_by_branch = defaultdict(list)
        for _, student in filtered_students.iterrows():
            student_info = {
                'roll_number': student.get('roll_number', student.get('id', 'N/A')),
                'name': student.get('name', 'Unknown'),
                'branch': student.get('branch', student.get('department', 'N/A')),
                'section': student.get('section', 'N/A'),
                'detained': False if not detained_column else 
                            str(student.get(detained_column, 'FALSE')).upper() in ['TRUE', '1', 'YES', 'Y']
            }
            students_by_branch[student_info['branch']].append(student_info)

        # Shuffle each branch
        for branch in students_by_branch:
            random.shuffle(students_by_branch[branch])

        # Create balanced distribution
        shuffled_students = create_optimal_branch_distribution(students_by_branch)

        # Prepare room info
        rooms = []
        for idx, room in rooms_df.iterrows():
            room_number = str(room.get('room_number', room.get('room_no', f"Room_{idx+1}")))
            capacity = int(room.get('capacity', room.get('seats', 30)))
            room_info = {
                'room_number': room_number,
                'room_name': str(room.get('room_name', room_number)),
                'capacity': capacity,
                'building': str(room.get('building', 'Main Building')),
                'floor': str(room.get('floor', '1'))
            }
            rooms.append(room_info)

        rooms.sort(key=lambda x: str(x['room_number']))

        # Generate seating plan
        seating_plan = []
        student_list = shuffled_students.copy()
        total_seated = 0

        for room in rooms:
            if not student_list:
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

            seats_filled = 0
            for row_num in range(rows):
                row = []
                for seat_num in range(seats_per_row):
                    if seats_filled >= room_capacity or not student_list:
                        row.append(None)
                        continue

                    # Find student with no branch conflict
                    student = find_suitable_student(student_list, room_seating['seats'], row, row_num, seat_num)
                    if student:
                        row.append(student)
                        student_list.remove(student)
                        total_seated += 1
                        seats_filled += 1
                    else:
                        row.append(None)

                room_seating['seats'].append(row)

            room_seating['students_count'] = seats_filled
            seating_plan.append(room_seating)

        unseated_students = student_list

        print("\n=== SEATING PLAN SUMMARY ===")
        print(f"Total students seated: {total_seated}")
        print(f"Total unseated students: {len(unseated_students)}")
        print(f"Total rooms used: {len(seating_plan)}")

        return seating_plan, unseated_students, None

    except Exception as e:
        return [], [], f"Error generating seating plan: {str(e)}"

def create_optimal_branch_distribution(students_by_branch):
    """
    Distribute students across branches (round-robin)
    """
    branch_queues = {b: deque(s) for b, s in students_by_branch.items()}
    distributed = []

    while any(branch_queues.values()):
        sorted_branches = sorted(branch_queues.items(), key=lambda x: len(x[1]), reverse=True)
        for branch, queue in sorted_branches:
            if queue:
                distributed.append(queue.popleft())

    return distributed

def find_suitable_student(student_list, room_seats, current_row, row_num, seat_num):
    """
    Pick a student ensuring no same-branch left-right or front-back
    """
    adjacent_branches = set()

    # Left
    if seat_num > 0 and current_row[seat_num - 1]:
        adjacent_branches.add(current_row[seat_num - 1]['branch'])
    # Right
    if seat_num < len(current_row) - 1 and current_row[seat_num]:
        adjacent_branches.add(current_row[seat_num]['branch'])
    # Above
    if row_num > 0 and seat_num < len(room_seats[row_num - 1]):
        above = room_seats[row_num - 1][seat_num]
        if above:
            adjacent_branches.add(above['branch'])

    # Choose student not in adjacent branches
    suitable = [s for s in student_list if s['branch'] not in adjacent_branches]
    if suitable:
        return random.choice(suitable)

    return None  # fallback: no suitable student

def get_room_summary(seating_plan):
    """
    Summary of room allocation
    """
    summary = []
    total_students = 0
    for room in seating_plan:
        count = room['students_count']
        total_students += count
        summary.append({
            'room_number': room['room_number'],
            'room_name': room['room_name'],
            'capacity': room['capacity'],
            'students_seated': count,
            'utilization': f"{(count / room['capacity'] * 100):.1f}%"
        })
    return summary, total_students
