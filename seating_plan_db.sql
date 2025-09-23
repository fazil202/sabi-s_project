-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 23, 2025 at 03:33 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `seating_plan_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `activity_logs`
--

CREATE TABLE `activity_logs` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `action` varchar(100) NOT NULL,
  `details` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `activity_logs`
--

INSERT INTO `activity_logs` (`id`, `user_id`, `action`, `details`, `ip_address`, `user_agent`, `created_at`) VALUES
(1, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-23 12:19:59'),
(2, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-23 12:19:59'),
(3, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 0 students in 3 rooms', NULL, NULL, '2025-09-23 12:20:41'),
(4, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 0 students in 3 rooms', NULL, NULL, '2025-09-23 12:22:40'),
(5, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-23 12:33:36'),
(6, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.104.1 Chrome/138.0.7204.235 Electron/37.3.1 Safari/537.36', '2025-09-23 12:33:36'),
(7, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-23 12:34:07'),
(8, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Code/1.104.1 Chrome/138.0.7204.235 Electron/37.3.1 Safari/537.36', '2025-09-23 12:34:07'),
(9, 1, 'LOGOUT', 'User admin logged out', NULL, NULL, '2025-09-23 12:34:33'),
(10, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-23 12:34:36'),
(11, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-23 12:34:36'),
(12, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 0 students in 3 rooms', NULL, NULL, '2025-09-23 12:34:54'),
(13, 1, 'PDF_GENERATED', 'PDF seating_plan_20250923_180457.pdf generated with 0 students in 3 rooms', NULL, NULL, '2025-09-23 12:34:57'),
(14, 1, 'LOGOUT', 'User admin logged out', NULL, NULL, '2025-09-23 12:46:39'),
(15, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-23 12:47:36'),
(16, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-23 12:47:36');

-- --------------------------------------------------------

--
-- Table structure for table `email_notifications`
--

CREATE TABLE `email_notifications` (
  `id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `recipient_email` varchar(100) NOT NULL,
  `subject` varchar(255) NOT NULL,
  `body` text NOT NULL,
  `sent` tinyint(1) DEFAULT 0,
  `sent_at` timestamp NULL DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `login_attempts`
--

CREATE TABLE `login_attempts` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `success` tinyint(1) NOT NULL,
  `attempt_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login_attempts`
--

INSERT INTO `login_attempts` (`id`, `username`, `ip_address`, `success`, `attempt_time`) VALUES
(1, 'fazil', NULL, 0, '2025-09-23 12:13:49'),
(2, 'admin', NULL, 0, '2025-09-23 12:14:03'),
(3, 'admin', NULL, 0, '2025-09-23 12:14:27'),
(4, 'admin', NULL, 0, '2025-09-23 12:14:43'),
(5, 'admin', NULL, 0, '2025-09-23 12:19:58'),
(6, 'admin', NULL, 1, '2025-09-23 12:19:59'),
(7, 'admin', NULL, 0, '2025-09-23 12:33:36'),
(8, 'admin', NULL, 1, '2025-09-23 12:33:36'),
(9, 'admin', NULL, 0, '2025-09-23 12:34:07'),
(10, 'admin', NULL, 1, '2025-09-23 12:34:07'),
(11, 'admin', NULL, 0, '2025-09-23 12:34:35'),
(12, 'admin', NULL, 1, '2025-09-23 12:34:36'),
(13, 'admin', NULL, 0, '2025-09-23 12:47:35'),
(14, 'admin', NULL, 1, '2025-09-23 12:47:36');

-- --------------------------------------------------------

--
-- Table structure for table `password_reset_tokens`
--

CREATE TABLE `password_reset_tokens` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `token` varchar(255) NOT NULL,
  `expires_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `used` tinyint(1) DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `pdf_history`
--

CREATE TABLE `pdf_history` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `filename` varchar(255) NOT NULL,
  `file_path` varchar(500) NOT NULL,
  `student_count` int(11) NOT NULL,
  `room_count` int(11) NOT NULL,
  `students_per_desk` int(11) NOT NULL,
  `include_detained` tinyint(1) NOT NULL,
  `building` varchar(100) DEFAULT NULL,
  `plan_details` text DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pdf_history`
--

INSERT INTO `pdf_history` (`id`, `user_id`, `filename`, `file_path`, `student_count`, `room_count`, `students_per_desk`, `include_detained`, `building`, `plan_details`, `created_at`) VALUES
(1, 1, 'seating_plan_20250923_180457.pdf', 'seating_plan_20250923_180457.pdf\\pdfs', 0, 3, 1, 0, 'Main Building', NULL, '2025-09-23 12:34:57');

-- --------------------------------------------------------

--
-- Table structure for table `rooms_config`
--

CREATE TABLE `rooms_config` (
  `id` int(11) NOT NULL,
  `room_number` varchar(50) NOT NULL,
  `building` varchar(100) DEFAULT NULL,
  `room_rows` int(11) NOT NULL,
  `room_columns` int(11) NOT NULL,
  `allowed_branches` text DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  `created_by` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `roll_number` varchar(50) NOT NULL,
  `name` varchar(100) NOT NULL,
  `branch` varchar(50) NOT NULL,
  `section` varchar(10) DEFAULT NULL,
  `is_detained` tinyint(1) DEFAULT 0,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `system_settings`
--

CREATE TABLE `system_settings` (
  `id` int(11) NOT NULL,
  `setting_key` varchar(100) NOT NULL,
  `setting_value` text DEFAULT NULL,
  `description` text DEFAULT NULL,
  `updated_by` int(11) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `system_settings`
--

INSERT INTO `system_settings` (`id`, `setting_key`, `setting_value`, `description`, `updated_by`, `updated_at`) VALUES
(1, 'students_per_desk', '1', 'Default number of students per desk', NULL, '2025-09-23 11:10:06'),
(2, 'include_detained', 'false', 'Include detained students in seating plans by default', NULL, '2025-09-23 11:10:06'),
(3, 'default_building', 'Main Building', 'Default building for seating arrangements', NULL, '2025-09-23 11:10:06'),
(4, 'session_timeout', '3600', 'Session timeout in seconds', NULL, '2025-09-23 11:10:06'),
(5, 'max_login_attempts', '5', 'Maximum login attempts before account lockout', NULL, '2025-09-23 11:10:06'),
(6, 'email_notifications', 'true', 'Enable email notifications', NULL, '2025-09-23 11:10:06'),
(7, 'password_min_length', '6', 'Minimum password length', NULL, '2025-09-23 11:10:06'),
(8, 'pdf_retention_days', '30', 'Number of days to retain PDF files', NULL, '2025-09-23 11:10:06');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `role` enum('admin','faculty','student') DEFAULT 'student',
  `is_active` tinyint(1) DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `email`, `password_hash`, `full_name`, `role`, `is_active`, `created_at`, `updated_at`) VALUES
(1, 'admin', 'admin@example.com', '$2b$12$cdoLjjHuqAd09S6xCMqdm.mHhVoaDAGAVJnPzYQTLfM3hFC9.ZnZa', 'Administrator', 'student', 1, '2025-09-23 07:25:14', '2025-09-23 12:19:26');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `email_notifications`
--
ALTER TABLE `email_notifications`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `login_attempts`
--
ALTER TABLE `login_attempts`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `token` (`token`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `pdf_history`
--
ALTER TABLE `pdf_history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `rooms_config`
--
ALTER TABLE `rooms_config`
  ADD PRIMARY KEY (`id`),
  ADD KEY `created_by` (`created_by`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `roll_number` (`roll_number`);

--
-- Indexes for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `setting_key` (`setting_key`),
  ADD KEY `updated_by` (`updated_by`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `activity_logs`
--
ALTER TABLE `activity_logs`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `email_notifications`
--
ALTER TABLE `email_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `login_attempts`
--
ALTER TABLE `login_attempts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pdf_history`
--
ALTER TABLE `pdf_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `rooms_config`
--
ALTER TABLE `rooms_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=233;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `activity_logs`
--
ALTER TABLE `activity_logs`
  ADD CONSTRAINT `activity_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `email_notifications`
--
ALTER TABLE `email_notifications`
  ADD CONSTRAINT `email_notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL;

--
-- Constraints for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  ADD CONSTRAINT `password_reset_tokens_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `pdf_history`
--
ALTER TABLE `pdf_history`
  ADD CONSTRAINT `pdf_history_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `rooms_config`
--
ALTER TABLE `rooms_config`
  ADD CONSTRAINT `rooms_config_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`);

--
-- Constraints for table `system_settings`
--
ALTER TABLE `system_settings`
  ADD CONSTRAINT `system_settings_ibfk_1` FOREIGN KEY (`updated_by`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
