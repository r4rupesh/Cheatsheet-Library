-- SQL Cheatsheet
-- The playground sample database includes departments and employees.

-- Select all columns or choose specific columns
SELECT * FROM employees;
SELECT name, title, salary FROM employees;

-- Filter and sort rows
SELECT name, salary
FROM employees
WHERE salary >= 80000
ORDER BY salary DESC;

-- Limit the number of rows
SELECT name, title
FROM employees
ORDER BY name
LIMIT 5;

-- Match text patterns and multiple conditions
SELECT name, title
FROM employees
WHERE title LIKE '%Engineer%'
  AND salary BETWEEN 70000 AND 120000;

-- Aggregate rows
SELECT COUNT(*) AS employee_count,
       ROUND(AVG(salary), 2) AS average_salary,
       MIN(salary) AS lowest_salary,
       MAX(salary) AS highest_salary
FROM employees;

-- Group and filter aggregates
SELECT department_id, COUNT(*) AS employee_count,
       ROUND(AVG(salary), 2) AS average_salary
FROM employees
GROUP BY department_id
HAVING COUNT(*) >= 2;

-- Join related tables
SELECT employees.name, departments.name AS department
FROM employees
JOIN departments ON employees.department_id = departments.department_id;

-- Use a left join to keep unmatched rows
SELECT departments.name AS department, employees.name AS employee
FROM departments
LEFT JOIN employees ON departments.department_id = employees.department_id;

-- Add conditional labels
SELECT name,
       CASE WHEN salary >= 100000 THEN 'Senior band' ELSE 'Standard band' END AS salary_band
FROM employees;

-- Common table expression (CTE)
WITH department_totals AS (
    SELECT department_id, SUM(salary) AS payroll
    FROM employees
    GROUP BY department_id
)
SELECT departments.name, department_totals.payroll
FROM department_totals
JOIN departments USING (department_id)
ORDER BY payroll DESC;

-- Subquery
SELECT name, salary
FROM employees
WHERE salary > (SELECT AVG(salary) FROM employees);

-- Handy scalar functions
SELECT UPPER(name) AS name_upper,
       LENGTH(name) AS name_length,
       ROUND(salary / 12, 2) AS monthly_salary
FROM employees;
