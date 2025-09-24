-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 24, 2025 at 05:15 AM
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
(31, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-24 01:01:59'),
(32, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 01:01:59'),
(33, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:02:11'),
(34, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:04:48'),
(35, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:04:54'),
(36, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:05:47'),
(37, 1, 'PDF_GENERATED', 'PDF seating_plan_20250923_180557.pdf generated with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:05:57'),
(38, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:11:47'),
(39, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:13:38'),
(40, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:17:52'),
(41, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:19:23'),
(42, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-24 01:19:36'),
(43, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 01:19:36'),
(44, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:19:57'),
(45, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-24 01:22:50'),
(46, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 01:22:50'),
(47, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 01:23:04'),
(48, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:26:56'),
(49, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:26:58'),
(50, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:26:59'),
(51, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:01'),
(52, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:02'),
(53, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:03'),
(54, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:05'),
(55, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:06'),
(56, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:07'),
(57, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:09'),
(58, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:10'),
(59, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:12'),
(60, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:13'),
(61, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:15'),
(62, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:16'),
(63, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:18'),
(64, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:19'),
(65, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:21'),
(66, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:22'),
(67, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:24'),
(68, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:25'),
(69, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:27'),
(70, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:28'),
(71, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:29'),
(72, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:30'),
(73, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:32'),
(74, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:33'),
(75, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:35'),
(76, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:36'),
(77, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:38'),
(78, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:39'),
(79, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:41'),
(80, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:42'),
(81, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:44'),
(82, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:45'),
(83, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:46'),
(84, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:47'),
(85, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:27:49'),
(86, 1, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 01:41:13'),
(87, 1, 'LOGIN', 'User admin logged in successfully', NULL, NULL, '2025-09-24 02:09:31'),
(88, 1, 'LOGIN', 'User admin logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 02:09:31'),
(89, 1, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 02:18:27'),
(90, 1, 'LOGOUT', 'User admin logged out', NULL, NULL, '2025-09-24 02:50:26'),
(91, 3, 'USER_CREATED', 'New user safiha created with role admin', NULL, NULL, '2025-09-24 02:54:08'),
(92, 3, 'LOGIN', 'User safiha logged in successfully', NULL, NULL, '2025-09-24 02:54:15'),
(93, 3, 'LOGIN', 'User safiha logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 02:54:15'),
(94, 3, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 02:54:45'),
(95, 3, 'PDF_GENERATED', 'PDF seating_plan_20250923_195458.pdf generated with 15 students in 3 rooms', NULL, NULL, '2025-09-24 02:54:58'),
(96, 3, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 02:55:09'),
(97, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:56:52'),
(98, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:56:55'),
(99, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:56:58'),
(100, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:01'),
(101, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:04'),
(102, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:07'),
(103, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:10'),
(104, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:14'),
(105, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:17'),
(106, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:20'),
(107, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:23'),
(108, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:26'),
(109, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:29'),
(110, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:33'),
(111, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:36'),
(112, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:39'),
(113, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:42'),
(114, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:45'),
(115, 3, 'EMAIL_SENT', 'Seating plan sent to mudinjakandupidi040101@gmail.com', NULL, NULL, '2025-09-24 02:57:48'),
(116, 3, 'LOGOUT', 'User safiha logged out', NULL, NULL, '2025-09-24 03:00:41'),
(117, 3, 'LOGIN', 'User safiha logged in successfully', NULL, NULL, '2025-09-24 03:00:44'),
(118, 3, 'LOGIN', 'User safiha logged in', '127.0.0.1', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36', '2025-09-24 03:00:44'),
(119, 3, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 15 students in 3 rooms', NULL, NULL, '2025-09-24 03:03:47'),
(120, 3, 'SEATING_PLAN_GENERATED', 'Generated seating plan with 48 students in 3 rooms', NULL, NULL, '2025-09-24 03:08:04');

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
(17, 'admin', NULL, 0, '2025-09-24 00:43:44'),
(18, 'admin', NULL, 1, '2025-09-24 00:43:45'),
(19, 'admin', NULL, 0, '2025-09-24 01:01:59'),
(20, 'admin', NULL, 1, '2025-09-24 01:01:59'),
(21, 'admin', NULL, 0, '2025-09-24 01:19:36'),
(22, 'admin', NULL, 1, '2025-09-24 01:19:36'),
(23, 'admin', NULL, 0, '2025-09-24 01:22:50'),
(24, 'admin', NULL, 1, '2025-09-24 01:22:50'),
(25, 'admin', NULL, 0, '2025-09-24 02:09:31'),
(26, 'admin', NULL, 1, '2025-09-24 02:09:31'),
(27, 'safiha', NULL, 0, '2025-09-24 02:54:15'),
(28, 'safiha', NULL, 1, '2025-09-24 02:54:15'),
(29, 'safiha', NULL, 0, '2025-09-24 03:00:44'),
(30, 'safiha', NULL, 1, '2025-09-24 03:00:44');

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
(3, 1, 'seating_plan_20250923_180557.pdf', 'D:\\Development\\Sheerin\\Sabi\'s Project\\seating_arrangements\\data\\pdfs\\seating_plan_20250923_180557.pdf', 15, 3, 1, 0, 'Main Building', NULL, '2025-09-24 01:05:57'),
(4, 3, 'seating_plan_20250923_195458.pdf', 'D:\\Development\\Sheerin\\Sabi\'s Project\\seating_arrangements\\data\\pdfs\\seating_plan_20250923_195458.pdf', 15, 3, 1, 0, 'Main Building', NULL, '2025-09-24 02:54:58');

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

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`id`, `roll_number`, `name`, `branch`, `section`, `is_detained`, `email`, `created_at`) VALUES
(1, '229X1A2901', 'Aditi', 'CS', 'A', 1, 'mudinjakandupidi040101@gmail.com', '2025-09-24 01:02:11'),
(192, '229X1A2902', 'Bharat', 'CS', 'A', 0, 'nan', '2025-09-24 02:18:27'),
(193, '229X1A2905', 'Charan', 'CS', 'A', 0, 'nan', '2025-09-24 02:18:27'),
(194, '229X1A2906', 'Deepa', 'CS', 'A', 1, 'nan', '2025-09-24 02:18:27'),
(195, '229X1A2907', 'Eshan', 'CS', 'A', 1, 'nan', '2025-09-24 02:18:27'),
(196, '229X1A2908', 'Farah', 'CS', 'B', 1, 'nan', '2025-09-24 02:18:27'),
(197, '229X1A2909', 'Guru', 'CS', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(198, '229X1A2910', 'Hari', 'CS', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(199, '229X1A2912', 'Isha', 'CS', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(200, '229X1A2915', 'Jyoti', 'CS', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(201, '229X1A2916', 'Karan', 'ME', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(202, '229X1A2917', 'Lina', 'ME', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(203, '229X1A2918', 'Mafalsej', 'ME', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(204, '229X1A2920', 'Neha', 'ME', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(205, '229X1A2922', 'Om', 'ME', 'A', 0, 'nan', '2025-09-24 02:18:27'),
(206, '239X5A02C3', 'santa', 'EC', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(207, '239X5A02C5', 'puwin', 'EC', 'B', 0, 'nan', '2025-09-24 02:18:27'),
(208, '239X5A02D0', 'dunk', 'EC', 'A', 0, 'nan', '2025-09-24 02:18:27'),
(209, '239X5A02D6', 'archen', 'EC', 'A', 0, 'nan', '2025-09-24 02:18:27');

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
(65, 'students_per_desk', '1', 'Default number of students per desk', NULL, '2025-09-24 00:58:45'),
(66, 'include_detained', 'false', 'Include detained students in seating plans by default', NULL, '2025-09-24 00:58:45'),
(67, 'default_building', 'Main Building', 'Default building for seating arrangements', NULL, '2025-09-24 00:58:45'),
(68, 'session_timeout', '3600', 'Session timeout in seconds', NULL, '2025-09-24 00:58:45'),
(69, 'max_login_attempts', '5', 'Maximum login attempts before account lockout', NULL, '2025-09-24 00:58:45'),
(70, 'email_notifications', 'true', 'Enable email notifications', NULL, '2025-09-24 00:58:45'),
(71, 'password_min_length', '6', 'Minimum password length', NULL, '2025-09-24 00:58:45'),
(72, 'pdf_retention_days', '30', 'Number of days to retain PDF files', NULL, '2025-09-24 00:58:45');

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
(1, 'admin', 'admin@example.com', '$2b$12$cdoLjjHuqAd09S6xCMqdm.mHhVoaDAGAVJnPzYQTLfM3hFC9.ZnZa', 'Administrator', 'student', 1, '2025-09-23 07:25:14', '2025-09-23 12:19:26'),
(3, 'safiha', 'safihatech@gmail.com', '$2b$12$Pco0T4zGOjKEKMQZnnFX0uFB1DQeaEHX6OxXmYKufG/ESUzmNrstC', 'safiha', 'admin', 1, '2025-09-24 02:54:08', '2025-09-24 02:54:08');

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
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=121;

--
-- AUTO_INCREMENT for table `email_notifications`
--
ALTER TABLE `email_notifications`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `login_attempts`
--
ALTER TABLE `login_attempts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `password_reset_tokens`
--
ALTER TABLE `password_reset_tokens`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `pdf_history`
--
ALTER TABLE `pdf_history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `rooms_config`
--
ALTER TABLE `rooms_config`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=381;

--
-- AUTO_INCREMENT for table `system_settings`
--
ALTER TABLE `system_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=257;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

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
