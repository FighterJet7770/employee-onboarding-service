CREATE TABLE IF NOT EXISTS departments (
    id INTEGER PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS onboarding_tasks (
    id INTEGER PRIMARY KEY,
    code VARCHAR(50) NOT NULL UNIQUE,
    title VARCHAR(120) NOT NULL,
    description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    first_name VARCHAR(80) NOT NULL,
    last_name VARCHAR(80) NOT NULL,
    email VARCHAR(180) NOT NULL UNIQUE,
    status VARCHAR(20) NOT NULL,
    department_id INTEGER NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
);

CREATE TABLE IF NOT EXISTS employee_tasks (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    task_id INTEGER NOT NULL,
    status VARCHAR(20) NOT NULL,
    UNIQUE (employee_id, task_id),
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (task_id) REFERENCES onboarding_tasks(id)
);

CREATE TABLE IF NOT EXISTS document_submissions (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    document_type VARCHAR(80) NOT NULL,
    reference_id VARCHAR(120) NOT NULL,
    status VARCHAR(20) NOT NULL,
    UNIQUE (employee_id, document_type),
    FOREIGN KEY (employee_id) REFERENCES employees(id)
);
