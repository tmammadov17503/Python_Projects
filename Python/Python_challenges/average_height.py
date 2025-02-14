print("Please, input heights:\n")
student_heights = input().split()
for n in range(0, len(student_heights)):
    student_heights[n] = int(student_heights[n])

total_height = sum(student_heights)
average_height = round(total_height / len(student_heights))
num_student = 0
for num in range(0, len(student_heights)):
    num_student += 1
print(f'total height = {total_height}')
print(f'number of people = {num_student}')
print(f'average height = {average_height}')


# total_height = 0
# for height in student_heights:
#   total_height += height
# print(f"total height = {total_height}")
#
# number_of_students = 0
# for student in student_heights:
#   number_of_students += 1
# print(f"number of students = {number_of_students}")
#
# average_height = round(total_height / number_of_students)
# print(f"average height = {average_height}")