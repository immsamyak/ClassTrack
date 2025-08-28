-- phpMyAdmin SQL Dump
-- version 5.2.2
-- https://www.phpmyadmin.net/
--
-- Host: mysql:3306
-- Generation Time: Aug 28, 2025 at 05:01 AM
-- Server version: 8.0.43
-- PHP Version: 8.2.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `classtrack_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `attendance`
--

CREATE TABLE `attendance` (
  `attendance_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `subject_id` int DEFAULT NULL,
  `attendance_date` date NOT NULL,
  `status` enum('present','absent') NOT NULL,
  `marked_by` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `attendance`
--

INSERT INTO `attendance` (`attendance_id`, `student_id`, `subject_id`, `attendance_date`, `status`, `marked_by`) VALUES
(10, 1, 1, '2025-08-28', 'present', 167),
(11, 2, 1, '2025-08-28', 'present', 167),
(12, 3, 1, '2025-08-28', 'present', 167),
(13, 4, 1, '2025-08-28', 'present', 167),
(14, 5, 1, '2025-08-28', 'present', 167);

-- --------------------------------------------------------

--
-- Table structure for table `marks`
--

CREATE TABLE `marks` (
  `mark_id` int NOT NULL,
  `student_id` int DEFAULT NULL,
  `subject_id` int DEFAULT NULL,
  `exam_type` varchar(50) NOT NULL,
  `marks_obtained` decimal(5,2) NOT NULL,
  `total_marks` decimal(5,2) NOT NULL,
  `grade` varchar(2) DEFAULT NULL,
  `exam_date` date DEFAULT NULL,
  `entered_by` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `marks`
--

INSERT INTO `marks` (`mark_id`, `student_id`, `subject_id`, `exam_type`, `marks_obtained`, `total_marks`, `grade`, `exam_date`, `entered_by`) VALUES
(1, 1, 3, 'Assignment', 100.00, 100.00, NULL, '2025-08-28', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `settings`
--

CREATE TABLE `settings` (
  `setting_id` int NOT NULL,
  `setting_name` varchar(100) NOT NULL,
  `setting_value` text,
  `setting_description` varchar(255) DEFAULT NULL,
  `updated_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `settings`
--

INSERT INTO `settings` (`setting_id`, `setting_name`, `setting_value`, `setting_description`, `updated_date`) VALUES
(98, 'school_name', 'KFA', NULL, '2025-08-28 03:55:05'),
(99, 'school_address', 'Mid Baneshwor', NULL, '2025-08-28 03:55:05'),
(100, 'school_phone', '9876543210', NULL, '2025-08-28 03:55:05'),
(101, 'school_email', 'info@kfaltd.com', NULL, '2025-08-28 03:55:05'),
(102, 'principal_name', 'IDK', NULL, '2025-08-28 03:55:05');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `student_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `roll_number` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `address` text,
  `enrollment_date` date DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT 'Male',
  `date_of_birth` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `guardian_name` varchar(100) DEFAULT NULL,
  `guardian_phone` varchar(15) DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `emergency_contact` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`student_id`, `user_id`, `roll_number`, `full_name`, `class_name`, `phone`, `address`, `enrollment_date`, `gender`, `date_of_birth`, `email`, `guardian_name`, `guardian_phone`, `blood_group`, `emergency_contact`) VALUES
(1, 162, 'LC000123', 'Samyak k Chaudhary', 'BCSIT 2nd Sem', '987654321', NULL, '2025-08-28', 'Male', NULL, 'samyakchy1@gmail.com', NULL, NULL, NULL, NULL),
(2, 163, 'LC000124', 'Sarasswoti Shrestha', 'BCSIT 2nd Sem', '987654321', NULL, '2025-08-28', 'Female', NULL, 'swoti@gmail.com', NULL, NULL, NULL, NULL),
(3, 164, 'LC000125', 'Manjit Khadka', 'BCSIT 2nd Sem', '987654321', NULL, '2025-08-28', 'Male', NULL, 'manjit@gmail.com', NULL, NULL, NULL, NULL),
(4, 165, 'LC000126', 'Alisha Thapa', 'BCSIT 2nd Sem', '987654321', NULL, '2025-08-28', 'Female', NULL, 'alisha@gmail.com', NULL, NULL, NULL, NULL),
(5, 1, 'TEST001', 'Test Student', 'BCSIT 2nd Sem', NULL, NULL, '2025-08-28', 'Male', NULL, NULL, NULL, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `subjects`
--

CREATE TABLE `subjects` (
  `subject_id` int NOT NULL,
  `subject_name` varchar(100) NOT NULL,
  `subject_code` varchar(20) NOT NULL,
  `class_name` varchar(50) NOT NULL,
  `teacher_id` int DEFAULT NULL,
  `credit_hours` int DEFAULT '3',
  `description` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `subjects`
--

INSERT INTO `subjects` (`subject_id`, `subject_name`, `subject_code`, `class_name`, `teacher_id`, `credit_hours`, `description`) VALUES
(1, 'Advance Computer Architecture', 'ACA123', 'BCSIT 2nd Sem', 166, 4, NULL),
(2, 'Operating System', 'OS123', 'BCSIT 2nd Sem', 166, 3, NULL),
(3, 'Python', 'PYN123', 'BCSIT 2nd Sem', 166, 3, NULL),
(5, 'Advanced Computer Network', 'ACN123', 'BCSIT 2nd Sem', 166, 4, NULL),
(6, 'Security in Computing', 'CIC123', 'BCSIT 2nd Sem', 166, 4, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `teachers`
--

CREATE TABLE `teachers` (
  `teacher_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `employee_id` varchar(20) NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `gender` enum('Male','Female','Other') NOT NULL,
  `date_of_birth` date DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(15) DEFAULT NULL,
  `department` varchar(50) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  `specialization` varchar(200) DEFAULT NULL,
  `experience_years` int DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  `address` text,
  `hire_date` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `teachers`
--

INSERT INTO `teachers` (`teacher_id`, `user_id`, `employee_id`, `full_name`, `gender`, `date_of_birth`, `email`, `phone`, `department`, `qualification`, `specialization`, `experience_years`, `salary`, `address`, `hire_date`) VALUES
(4, 166, 'XXX123', 'Ripesh Sir', 'Male', NULL, 'ripesh@kfaltd.com', '987654321', 'IT', NULL, 'Security in Computing', NULL, 100000.00, NULL, '2025-08-28');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('admin','teacher','student') NOT NULL,
  `full_name` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `role`, `full_name`, `email`, `created_date`) VALUES
(1, 'test_student', 'password', 'student', 'Test Student', 'test@email.com', '2025-08-28 04:19:06'),
(162, 'lc000123', 'student123', 'student', 'Samyak k Chaudhary', 'samyakchy1@gmail.com', '2025-08-28 04:03:03'),
(163, 'lc000124', 'student123', 'student', 'Sarasswoti Shrestha', 'swoti@gmail.com', '2025-08-28 04:03:03'),
(164, 'lc000125', 'student123', 'student', 'Manjit Khadka', 'manjit@gmail.com', '2025-08-28 04:03:03'),
(165, 'lc000126', 'student123', 'student', 'Alisha Thapa', 'alisha@gmail.com', '2025-08-28 04:03:03'),
(166, 'xxx123', 'teacher123', 'teacher', 'Ripesh Sir', 'ripesh@kfaltd.com', '2025-08-28 04:03:03'),
(167, 'admin', 'admin', 'admin', 'Administrator', 'admin@classtrack.com', '2025-08-28 04:05:42'),
(168, 'teacher1', 'teacher123', 'teacher', 'John Smith', 'john@classtrack.com', '2025-08-28 04:05:42');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `attendance`
--
ALTER TABLE `attendance`
  ADD PRIMARY KEY (`attendance_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `marked_by` (`marked_by`);

--
-- Indexes for table `marks`
--
ALTER TABLE `marks`
  ADD PRIMARY KEY (`mark_id`),
  ADD KEY `student_id` (`student_id`),
  ADD KEY `subject_id` (`subject_id`),
  ADD KEY `entered_by` (`entered_by`);

--
-- Indexes for table `settings`
--
ALTER TABLE `settings`
  ADD PRIMARY KEY (`setting_id`),
  ADD UNIQUE KEY `setting_name` (`setting_name`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`student_id`),
  ADD UNIQUE KEY `roll_number` (`roll_number`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `subjects`
--
ALTER TABLE `subjects`
  ADD PRIMARY KEY (`subject_id`),
  ADD UNIQUE KEY `subject_code` (`subject_code`),
  ADD KEY `teacher_id` (`teacher_id`);

--
-- Indexes for table `teachers`
--
ALTER TABLE `teachers`
  ADD PRIMARY KEY (`teacher_id`),
  ADD UNIQUE KEY `employee_id` (`employee_id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `attendance`
--
ALTER TABLE `attendance`
  MODIFY `attendance_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `marks`
--
ALTER TABLE `marks`
  MODIFY `mark_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `settings`
--
ALTER TABLE `settings`
  MODIFY `setting_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=103;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `student_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `subjects`
--
ALTER TABLE `subjects`
  MODIFY `subject_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=32;

--
-- AUTO_INCREMENT for table `teachers`
--
ALTER TABLE `teachers`
  MODIFY `teacher_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=175;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `attendance`
--
ALTER TABLE `attendance`
  ADD CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`),
  ADD CONSTRAINT `attendance_ibfk_3` FOREIGN KEY (`marked_by`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `marks`
--
ALTER TABLE `marks`
  ADD CONSTRAINT `marks_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  ADD CONSTRAINT `marks_ibfk_2` FOREIGN KEY (`subject_id`) REFERENCES `subjects` (`subject_id`),
  ADD CONSTRAINT `marks_ibfk_3` FOREIGN KEY (`entered_by`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `students_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `subjects`
--
ALTER TABLE `subjects`
  ADD CONSTRAINT `subjects_ibfk_1` FOREIGN KEY (`teacher_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `teachers`
--
ALTER TABLE `teachers`
  ADD CONSTRAINT `teachers_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
