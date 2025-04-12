-- select * from students
-- select distinct gender from students
-- select distinct courses from courses
-- select distinct grade from enrollments

-- select * from courses order by credits desc limit 3
-- select name from students order by name limit 10
-- select * from majors order by major_id limit 5

-- select * from students where total_credits in(select MAX(total_credits) from students)
-- select * from courses where credits in(select min(credits) from courses)
-- select major_name from majors where major_id in(select min(major_id) from majors)

-- select sum(credits)from courses
-- select sum(grade)from enrollments
-- select sum (total_credits)from students where age = 20

-- select * from courses where credits in (3, 4, 6)
-- select * from students where name IN ('Alice','Bob', 'Eve')
-- select * from enrollments where grade in (3.64, 2.18, 3.37)

-- select * from students where total_credits between 50 and 100
-- select * from courses where credits between 2 and 5
-- select * from enrollments where grade between 3.0 and 4.0

-- select student_id as "ID", name as "Student Name", age as "Student Age" from students
-- select course_id as "ID", course_name as "Course", credits as "Credit hours" from courses
-- select major_id as "Major code", major_name as "Major Description" from majors

-- select name, course_name from students inner join enrollments on students.student_id = enrollments.student_id inner join courses on courses.course_id = enrollments.course_id
-- select name, major_name from students inner join majors on students.major_id = majors.major_id
-- select name, grade, course_name from students inner join enrollments on students.student_id = enrollments.student_id inner join courses on courses.course_id = enrollments.course_id

-- select name, major_name from students left join majors on students.major_id = majors.major_id
-- select name, course_name from courses left join enrollments on courses.course_id = enrollments.course_id left join students on students.student_id = enrollments.student_id
-- select name, major_name from majors left join students on students.major_id = majors.major_id

-- select name, major_name from students right join majors on students.major_id = majors.major_id
-- select distinct course_name from enrollments right join courses on courses.course_id = enrollments.course_id
-- select name, course_name from courses right join enrollments on courses.course_id = enrollments.course_id right join students on students.student_id = enrollments.student_id

-- select name, course_name from courses full join enrollments on courses.course_id = enrollments.course_id full join students on students.student_id = enrollments.student_id
-- select name, major_name from students full join majors on students.major_id = majors.major_id
-- select enrollment_id, course_name from courses full join enrollments on courses.course_id = enrollments.course_id

-- select name, course_name from students cross join courses limit 10
-- select name, major_name from students cross join majors
-- select name, course_name from students cross join courses order by student_id

-- select gender, avg(age) from students group by gender
-- select count(course_name), credits from courses group by credits
-- select major_name, sum(total_credits) from students left join majors on students.major_id = majors.major_id group by students.major_id, major_name

-- select count(course_name), credits from courses group by credits having count(course_name) > 2
-- select count(student_id), students.major_id, major_name from students right join majors on students.major_id = majors.major_id group by students.major_id, major_name having count(student_id) > 5
-- select name, avg(grade) from students inner join enrollments on students.student_id = enrollments.student_id group by name having avg(grade) > 3

-- select name, age from students order by age
-- select course_name, credits from courses order by credits desc
-- select * from enrollments order by grade, student_id



--- select top 5 students and sort by total credits descending
-- select * from students order by total_credits desc limit 5 offset 5
