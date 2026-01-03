-- HR.EMPLOYEES HR.JOBS, and HR.DEPARTMENTS tables

-- 2 phase
SELECT emp.EMPLOYEE_ID, emp.FIRST_NAME, emp.LAST_NAME, emp.JOB_ID, job.JOB_TITLE, emp.DEPARTMENT_ID, dep.DEPARTMENT_NAME, emp.SALARY,
MIN(emp.SALARY) OVER (PARTITION BY emp.JOB_ID) AS min_salary_for_job_id, -- for the minimum salary
MAX(emp.SALARY) OVER (PARTITION BY emp.JOB_ID) AS max_salary_for_job_id, -- for the maximum salary
ROUND(AVG(emp.SALARY) OVER (PARTITION BY emp.JOB_ID), 2) AS avg_salary_for_job_id, -- for average salary

-- phase 3
CASE
WHEN COUNT(DISTINCT emp.DEPARTMENT_ID) OVER (PARTITION BY emp.JOB_ID) = 1 THEN 'YES' ELSE 'NO'
END AS low_job_distribution

-- for the 1 phase
FROM HR.EMPLOYEES AS emp
JOIN HR.JOBS AS job ON emp.JOB_ID = job.JOB_ID
JOIN HR.DEPARTMENTS AS dep ON emp.DEPARTMENT_ID = dep.DEPARTMENT_ID

-- phase 4
ORDER BY emp.SALARY DESC; 