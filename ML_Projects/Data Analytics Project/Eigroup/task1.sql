-- HR.EMPLOYEES and HR.DEPARTMENTS tables

-- for the 2 phase
SELECT dep.DEPARTMENT_NAME AS department_name, AVG(emp.SALARY) AS avg_salary, MAX(emp.SALARY) AS max_salary,
MIN(emp.SALARY) AS min_salary, -- average, maximum, and minimum salary found

MAX(CASE
    WHEN emp.SALARY = MAX(emp.SALARY) OVER (PARTITION BY emp.DEPARTMENT_ID)
    THEN emp.FIRST_NAME || ' ' || emp.LAST_NAME END) AS employee_name_with_max_salary, -- person with the max salary

MAX(CASE 
    WHEN emp.SALARY = MIN(emp.SALARY) OVER (PARTITION BY emp.DEPARTMENT_ID) 
    THEN emp.FIRST_NAME || ' ' || emp.LAST_NAME END) AS employee_name_with_min_salary, -- person with the min salary
           
-- for the 3rd phase
COUNT(emp.EMPLOYEE_ID) AS emp_count, SUM(emp.SALARY) AS emp_total_salary,
((COUNT(emp.EMPLOYEE_ID) * MAX(emp.SALARY)) - SUM(emp.SALARY)) AS cost_increase, -- final calculation here
-- ((emp_count * max_salary) - emp_total_salary) as cost_inscrease [mainly this is how it looks just we can not use aliases]

-- for the phase 4
ROUND(((COUNT(emp.EMPLOYEE_ID) * MAX(emp.SALARY) - SUM(emp.SALARY)) / SUM(emp.SALARY)) * 100,2) 
as cost_increase_percent -- percentage finding [without rounding would be a huge number]

-- for the 1 phase
FROM HR.EMPLOYEES AS emp -- emp for empoyees 
JOIN HR.DEPARTMENTS AS dep ON emp.DEPARTMENT_ID = dep.DEPARTMENT_ID -- dep for departments 
-- combine both based on the employees department id 

-- phase 2
GROUP BY dep.DEPARTMENT_NAME; -- we have to use it because we used aggregates (AVG, MAX, MIN)