import pandas as pd
import math
from collections import deque, defaultdict

def parse_roll_number(roll_value):
    if pd.isna(roll_value):
        return float('inf')
    text = str(roll_value).strip()
    if not text:
        return float('inf')
    try:
        return int(text)
    except ValueError:
        digits = ''.join(ch for ch in text if ch.isdigit())
        if digits:
            return int(digits)
        return float('inf')

def normalize_branch(branch):
    if branch is None:
        return 'UNKNOWN'
    text = str(branch).strip()
    return text.upper() if text else 'UNKNOWN'

def pick_next_branch(branches, branch_queues, start_idx, disallowed):
    if not branches:
        return None, start_idx
    total = len(branches)
    idx = start_idx % total
    fallback = None
    fallback_idx = None
    checked = 0

    while checked < total:
        branch = branches[idx]
        if branch_queues[branch]:
            if branch not in disallowed:
                return branch, (idx + 1) % total
            if fallback is None:
                fallback = branch
                fallback_idx = idx
        idx = (idx + 1) % total
        checked += 1

    if fallback is not None:
        return fallback, (fallback_idx + 1) % total
    return None, start_idx

def generate_seating_plan(student_csv_path, room_csv_path, students_per_desk=1, include_detained=False):
    """
    Generate seating plan with alternating branches and sequential roll numbers.
    """
    try:
        students_df = pd.read_csv(student_csv_path)
        rooms_df = pd.read_csv(room_csv_path)

        students_df.columns = students_df.columns.str.lower().str.strip()
        rooms_df.columns = rooms_df.columns.str.lower().str.strip()

        detained_column = None
        for col in students_df.columns:
            if 'detained' in col.lower():
                detained_column = col
                break

        if include_detained or not detained_column:
            filtered_students = students_df.copy()
        else:
            detained_mask = students_df[detained_column].astype(str).str.upper().isin(['TRUE', '1', 'YES', 'Y'])
            filtered_students = students_df[~detained_mask]

        if len(filtered_students) == 0:
            return [], [], "No students available for seating."

        total_students_available = len(filtered_students)

        students_by_branch = defaultdict(list)
        for _, student in filtered_students.iterrows():
            roll_value = student.get('roll_number', student.get('id', 'N/A'))
            roll_text = str(roll_value).strip() if not pd.isna(roll_value) else 'N/A'
            branch = normalize_branch(student.get('branch', student.get('department', '')))

            student_info = {
                'roll_number': roll_text if roll_text else 'N/A',
                'name': str(student.get('name', 'Unknown')).strip() or 'Unknown',
                'branch': branch,
                'section': str(student.get('section', 'N/A')).strip() or 'N/A',
                'detained': False if not detained_column else str(student.get(detained_column, 'FALSE')).upper() in ['TRUE', '1', 'YES', 'Y']
            }
            students_by_branch[branch].append(student_info)

        if not students_by_branch:
            return [], [], "No valid students found after grouping by branch."

        for branch, records in students_by_branch.items():
            records.sort(key=lambda s: (parse_roll_number(s['roll_number']), str(s['roll_number']).strip()))

        branch_queues = {branch: deque(records) for branch, records in students_by_branch.items()}
        branches = sorted(branch_queues.keys())

        if not branches:
            return [], [], "No valid branches found."

        rooms = []
        total_capacity = 0
        for idx, room in rooms_df.iterrows():
            room_number = str(room.get('room_number', room.get('room_no', f"Room_{idx + 1}")))
            capacity = int(room.get('capacity', room.get('seats', 30)))
            total_capacity += capacity
            room_info = {
                'room_number': room_number,
                'room_name': str(room.get('room_name', room_number)),
                'capacity': capacity,
                'building': str(room.get('building', 'Main Building')),
                'floor': str(room.get('floor', '1'))
            }
            rooms.append(room_info)

        rooms.sort(key=lambda x: x['room_number'])

        try:
            students_per_desk = int(students_per_desk)
        except (TypeError, ValueError):
            students_per_desk = 1
        students_per_desk = max(1, students_per_desk)

        seating_plan = []
        total_seated = 0
        branch_distribution = defaultdict(int)
        branch_idx = 0

        for room in rooms:
            if not any(branch_queues[branch] for branch in branches):
                break

            room_capacity = room['capacity']
            seats_per_row = 6
            rows = math.ceil(room_capacity / seats_per_row) if room_capacity else 0
            seat_grid = [[None for _ in range(seats_per_row)] for _ in range(rows)]
            seat_assignments = []
            seat_number = 1
            last_branch_used = None

            while seat_number <= room_capacity and any(branch_queues[branch] for branch in branches):
                active_branches = {b for b in branches if branch_queues[b]}
                if not active_branches:
                    break

                disallowed_first = set()
                if last_branch_used and len(active_branches) > 1:
                    disallowed_first.add(last_branch_used)

                branch_choice, branch_idx = pick_next_branch(branches, branch_queues, branch_idx, disallowed_first)
                if branch_choice is None:
                    break

                primary_student = dict(branch_queues[branch_choice].popleft())
                desk_students = [primary_student]
                desk_branches = {branch_choice}

                while len(desk_students) < students_per_desk:
                    active_branches = {b for b in branches if branch_queues[b]}
                    if not active_branches:
                        break

                    branch_choice_extra, branch_idx = pick_next_branch(branches, branch_queues, branch_idx, desk_branches)
                    if branch_choice_extra is None:
                        break

                    extra_student = dict(branch_queues[branch_choice_extra].popleft())
                    desk_students.append(extra_student)
                    desk_branches.add(branch_choice_extra)

                row_idx = (seat_number - 1) // seats_per_row
                col_idx = (seat_number - 1) % seats_per_row
                if row_idx < len(seat_grid):
                    seat_grid[row_idx][col_idx] = desk_students

                seat_assignments.append({
                    'seat_number': seat_number,
                    'students': desk_students
                })

                for assigned in desk_students:
                    branch_distribution[assigned['branch']] += 1
                total_seated += len(desk_students)
                last_branch_used = desk_students[0]['branch']
                seat_number += 1

            room_students_count = sum(len(seat['students']) for seat in seat_assignments)
            room_entry = {
                'room_number': room['room_number'],
                'room_name': room['room_name'],
                'building': room['building'],
                'floor': room['floor'],
                'capacity': room_capacity,
                'seats': seat_grid,
                'seat_assignments': seat_assignments,
                'students_count': room_students_count
            }
            seating_plan.append(room_entry)

        unseated_students = []
        for branch in branches:
            unseated_students.extend(dict(student) for student in branch_queues[branch])

        summary_stats = {
            'total_students_available': total_students_available,
            'total_students_seated': total_seated,
            'total_unseated': len(unseated_students),
            'total_capacity': total_capacity,
            'total_rooms': sum(1 for room in seating_plan if room['students_count'] > 0),
            'overall_utilization': round((total_seated / total_capacity * 100), 2) if total_capacity else 0,
            'branch_distribution': dict(branch_distribution),
            'students_per_desk': students_per_desk,
            'include_detained': include_detained
        }

        print("\n=== SEATING PLAN SUMMARY ===")
        print(f"Total students available: {total_students_available}")
        print(f"Total students seated: {total_seated}")
        print(f"Total unseated students: {len(unseated_students)}")
        print(f"Total rooms used: {summary_stats['total_rooms']}")
        print(f"Overall utilization: {summary_stats['overall_utilization']}%")
        print(f"Branch distribution: {summary_stats['branch_distribution']}")
        print(f"Students per desk setting: {students_per_desk}")

        return (seating_plan, summary_stats), unseated_students, None

    except Exception as e:
        print(f"Error in generate_seating_plan: {e}")
        import traceback
        traceback.print_exc()
        return [], [], f"Error generating seating plan: {str(e)}"

def get_room_summary(seating_plan):
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
            'utilization': f"{(count / room['capacity'] * 100):.1f}%" if room['capacity'] else "0.0%"
        })

    return summary, total_students
