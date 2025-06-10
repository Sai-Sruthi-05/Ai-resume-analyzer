-- Create resume_analyzer database if it doesn't exist
CREATE DATABASE IF NOT EXISTS resume_analyzer CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;

-- Use the database
USE resume_analyzer;

-- User Table
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Resume Table
CREATE TABLE IF NOT EXISTS resume (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    keywords TEXT NOT NULL,
    upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE SET NULL
);

-- Resource Table
CREATE TABLE IF NOT EXISTS resource (
    id INT AUTO_INCREMENT PRIMARY KEY,
    resume_id INT NOT NULL,
    category VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(512) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (resume_id) REFERENCES resume(id) ON DELETE CASCADE
);