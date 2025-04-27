import csv

def analyze_grades(file_path, threshold):
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            grades = list(map(int, row['grade'].split()))
            avg = sum(grades) / len(grades)
            if avg > threshold:
                print(f"Student {row['name']} with average {avg:.2f} is above threshold.")

# Usage
analyze_grades('students.csv', 75)
