"""
The provided code stub will read in a dictionary containing key/value pairs of name:[marks] for a list of students. Print the average of the marks array for the student name provided, showing 2 places after the decimal.


"""






n = int(input())
student_marks = {}
for _ in range(n):
    name, *line = input().split()
    scores = list(map(float, line))
    student_marks[name] = scores
query_name = input()
total_marks=list(student_marks[query_name])
addition=sum(total_marks)
average_mark=addition/len(student_marks[query_name])
print("{:.2f}".format(average_mark))