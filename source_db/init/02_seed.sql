INSERT INTO customers VALUES
(1, 'John', 'Smith', 'john.smith@email.com', 'Dallas', 'TX', NOW(), NOW()),
(2, 'Priya', 'Patel', 'priya.patel@email.com', 'Austin', 'TX', NOW(), NOW()),
(3, 'Michael', 'Brown', 'michael.brown@email.com', 'Seattle', 'WA', NOW(), NOW()),
(4, 'Sara', 'Wilson', 'sara.wilson@email.com', 'Chicago', 'IL', NOW(), NOW()),
(5, 'David', 'Lee', 'david.lee@email.com', 'San Jose', 'CA', NOW(), NOW());

INSERT INTO agents VALUES
(101, 'Alice Johnson', 'South', NOW(), NOW()),
(102, 'Brian Thomas', 'West', NOW(), NOW()),
(103, 'Carol Davis', 'Midwest', NOW(), NOW());

INSERT INTO policies VALUES
(1001, 1, 101, 'Auto', 1200.00, 'ACTIVE', '2025-01-01', '2025-12-31', NOW(), NOW()),
(1002, 2, 101, 'Health', 2400.00, 'ACTIVE', '2025-02-01', '2026-01-31', NOW(), NOW()),
(1003, 3, 102, 'Life', 1800.00, 'LAPSED', '2024-06-01', '2025-05-31', NOW(), NOW()),
(1004, 4, 103, 'Auto', 1500.00, 'ACTIVE', '2025-03-15', '2026-03-14', NOW(), NOW()),
(1005, 5, 102, 'Home', 2200.00, 'ACTIVE', '2025-04-01', '2026-03-31', NOW(), NOW());

INSERT INTO claims VALUES
(5001, 1001, 450.00, 'OPEN', '2025-03-01', NOW(), NOW(), NOW()),
(5002, 1002, 1200.00, 'CLOSED', '2025-03-10', NOW(), NOW(), NOW()),
(5003, 1004, 800.00, 'OPEN', '2025-03-18', NOW(), NOW(), NOW()),
(5004, 1005, 300.00, 'REJECTED', '2025-03-20', NOW(), NOW(), NOW());

INSERT INTO payments VALUES
(7001, 1001, 100.00, '2025-03-05', 'CARD', NOW(), NOW()),
(7002, 1002, 200.00, '2025-03-07', 'BANK_TRANSFER', NOW(), NOW()),
(7003, 1003, 150.00, '2025-03-09', 'CARD', NOW(), NOW()),
(7004, 1004, 175.00, '2025-03-15', 'UPI', NOW(), NOW()),
(7005, 1005, 220.00, '2025-03-21', 'CARD', NOW(), NOW());
