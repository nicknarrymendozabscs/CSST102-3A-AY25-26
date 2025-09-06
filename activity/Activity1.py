#!/usr/bin/env python3
"""
Mini Expert System for Student Rules - Improved Version
- Attendance Rule
- Grading Rule  
- Login System Rule
- Bonus Points Rule
- Library Borrowing Rule
All outcomes are logged to logic_results.csv
"""

import csv
import os
from datetime import datetime
from typing import Dict, Any, Tuple, Optional
from dataclasses import dataclass

# Configuration
CSV_PATH = os.path.join(os.path.expanduser("~"), "Downloads", "logic_results.csv")

@dataclass
class Student:
    """Data class for student information"""
    name: str
    attendance_pct: float
    final_grade: float
    username_ok: bool
    password_ok: bool
    is_locked: bool
    participated: bool
    base_score: float
    id_valid: bool
    has_overdue: bool

class ExpertSystem:
    """Expert System class for student rules evaluation"""
    
    def __init__(self, csv_path: str = CSV_PATH):
        self.csv_path = csv_path
        self.attendance_threshold = 75.0
        self.passing_grade = 75.0
        self.bonus_points = 5.0
        self.max_score = 100.0
    
    def attendance_rule(self, attendance_pct: float) -> Tuple[bool, str]:
        """
        Attendance Rule: If attendance >= 75% -> Eligible; else -> Not eligible
        """
        if not 0 <= attendance_pct <= 100:
            return False, f"Invalid attendance: {attendance_pct}%"
        
        ok = attendance_pct >= self.attendance_threshold
        return ok, f"attendance={attendance_pct:.1f}% -> {'eligible' if ok else 'not eligible'}"

    def grading_rule(self, final_grade: float) -> Tuple[bool, str]:
        """
        Grading Rule: If final grade >= 75 -> Passed; else -> Failed
        """
        if not 0 <= final_grade <= 100:
            return False, f"Invalid grade: {final_grade}"
        
        ok = final_grade >= self.passing_grade
        return ok, f"grade={final_grade:.1f} -> {'pass' if ok else 'fail'}"

    def login_system_rule(self, username_ok: bool, password_ok: bool, is_locked: bool) -> Tuple[bool, str]:
        """
        Login System Rule: If username valid AND password valid AND account not locked -> Success
        """
        ok = username_ok and password_ok and (not is_locked)
        detail = f"user_ok={username_ok}, pass_ok={password_ok}, locked={is_locked} -> {'login success' if ok else 'login denied'}"
        return ok, detail

    def bonus_points_rule(self, participated: bool, base_score: float) -> Tuple[bool, str]:
        """
        Bonus Points Rule: If participated -> add bonus points (capped to max_score)
        """
        if not 0 <= base_score <= 100:
            return False, f"Invalid base score: {base_score}"
        
        if participated:
            new_score = min(base_score + self.bonus_points, self.max_score)
            return True, f"participated={participated}, base={base_score} -> bonus +{self.bonus_points}, final={new_score}"
        else:
            return False, f"participated={participated}, base={base_score} -> no bonus, final={base_score}"

    def library_borrowing_rule(self, id_valid: bool, has_overdue: bool) -> Tuple[bool, str]:
        """
        Library Borrowing Rule: If ID valid AND no overdue items -> Allowed; else -> Not allowed
        """
        ok = id_valid and (not has_overdue)
        return ok, f"id_valid={id_valid}, overdue={has_overdue} -> {'allowed' if ok else 'not allowed'}"

    def evaluate_student(self, student: Student) -> Dict[str, Tuple[bool, str]]:
        """Evaluate all rules for a student"""
        results = {}
        
        try:
            results['AttendanceRule'] = self.attendance_rule(student.attendance_pct)
            results['GradingRule'] = self.grading_rule(student.final_grade)
            results['LoginSystemRule'] = self.login_system_rule(
                student.username_ok, student.password_ok, student.is_locked
            )
            results['BonusPointsRule'] = self.bonus_points_rule(student.participated, student.base_score)
            results['LibraryBorrowingRule'] = self.library_borrowing_rule(student.id_valid, student.has_overdue)
        except Exception as e:
            print(f"Error evaluating student {student.name}: {e}")
            
        return results

    def log_results(self, student_name: str, results: Dict[str, Tuple[bool, str]]) -> None:
        """Log evaluation results to CSV file"""
        fieldnames = [
            "timestamp", "student",
            "AttendanceRule", "AttendanceDetail",
            "GradingRule", "GradingDetail", 
            "LoginSystemRule", "LoginDetail",
            "BonusPointsRule", "BonusDetail",
            "LibraryBorrowingRule", "LibraryDetail"
        ]
        
        # Create mapping for detail field names
        detail_mapping = {
            'AttendanceRule': 'AttendanceDetail',
            'GradingRule': 'GradingDetail',
            'LoginSystemRule': 'LoginDetail',
            'BonusPointsRule': 'BonusDetail',
            'LibraryBorrowingRule': 'LibraryDetail'
        }
        
        try:
            # Check if file needs header
            need_header = not os.path.exists(self.csv_path) or os.path.getsize(self.csv_path) == 0
        except OSError:
            need_header = True

        try:
            with open(self.csv_path, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                if need_header:
                    writer.writeheader()
                
                row = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "student": student_name,
                }
                
                # Add rule results to row using proper mapping
                for rule_name, (result, detail) in results.items():
                    row[rule_name] = result
                    row[detail_mapping[rule_name]] = detail
                
                writer.writerow(row)
        except IOError as e:
            print(f"Error writing to CSV: {e}")

def demo():
    """Demonstration of the expert system"""
    system = ExpertSystem()
    
    test_students = [
        Student(
            name="Avellaneda",
            attendance_pct=82.5,
            final_grade=78.0,
            username_ok=True,
            password_ok=True,
            is_locked=False,
            participated=True,
            base_score=88.0,
            id_valid=True,
            has_overdue=False
        ),
        Student(
            name="Capili", 
            attendance_pct=70.0,
            final_grade=72.0,
            username_ok=True,
            password_ok=False,
            is_locked=False,
            participated=False,
            base_score=65.0,
            id_valid=True,
            has_overdue=True
        ),
        Student(
            name="Ramos",
            attendance_pct=95.0,
            final_grade=92.0,
            username_ok=True,
            password_ok=True,
            is_locked=True,
            participated=True,
            base_score=96.0,
            id_valid=False,
            has_overdue=False
        )
    ]

    print("=== Mini Expert System — Demo Run ===")
    print(f"CSV output: {system.csv_path}")
    
    for student in test_students:
        results = system.evaluate_student(student)
        system.log_results(student.name, results)
        
        print(f"\nStudent: {student.name}")
        for rule, (ok, detail) in results.items():
            status = "✓" if ok else "✗"
            print(f" {status} {rule:20}: {detail}")

    print(f"\nResults logged to: {system.csv_path}")

if __name__ == "__main__":
    # Clean start for demo (comment out to append to existing file)
    csv_path = CSV_PATH
    if os.path.exists(csv_path):
        os.remove(csv_path)
    
    demo()