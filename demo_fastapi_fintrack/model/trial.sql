-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 30, 2024 at 02:53 AM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.1.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `trial`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `admin_ID` int(10) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`admin_ID`, `firstname`, `lastname`, `email`, `password`) VALUES
(0, 'dsadas', 'sdadsa', 'dadada@gmail.com', ''),
(1, 'Jan Kurt', 'Gerongco', 'jgerongco@gmail.com', ''),
(2, 'Jd', 'boy', 'jd@gmail.com', '');

-- --------------------------------------------------------

--
-- Table structure for table `history`
--

CREATE TABLE `history` (
  `history_id` int(10) NOT NULL,
  `reservation_date` datetime NOT NULL,
  `user_id` int(10) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `email` varchar(255) NOT NULL,
  `faculty_in_charge` text NOT NULL,
  `purpose` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `history`
--

INSERT INTO `history` (`history_id`, `reservation_date`, `user_id`, `firstname`, `lastname`, `email`, `faculty_in_charge`, `purpose`) VALUES
(1, '2024-03-06 13:06:39', 1, 'John', 'Doe', 'john.doe@example.com', 'hakdog', 'Meeting'),
(2, '2024-03-29 06:11:48', 3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'James', 'Special Exam');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `report_id` int(10) NOT NULL,
  `user_id` bigint(10) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `violation` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`report_id`, `user_id`, `firstname`, `lastname`, `violation`) VALUES
(1, 1, 'John ', 'Doe', 'Vandalism'),
(2, 3, 'Alice', 'Johnson', 'Leaving the Aircon Open');

-- --------------------------------------------------------

--
-- Table structure for table `reservation`
--

CREATE TABLE `reservation` (
  `reservation_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `faculty_in_charge` text NOT NULL,
  `number_of_people` int(100) NOT NULL,
  `reservation_date` datetime NOT NULL,
  `purpose` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `reservation`
--

INSERT INTO `reservation` (`reservation_id`, `user_id`, `firstname`, `lastname`, `email`, `faculty_in_charge`, `number_of_people`, `reservation_date`, `purpose`) VALUES
(1, 1, 'John', 'Doe', 'john.doe@example.com', 'hakdog', 12, '2024-03-06 13:06:39', 'Meeting'),
(2, 3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'James', 5, '2024-03-29 06:11:48', 'Special Exam');

-- --------------------------------------------------------

--
-- Table structure for table `schedule`
--

CREATE TABLE `schedule` (
  `schedule_id` int(10) NOT NULL,
  `reservation_id` int(10) NOT NULL,
  `user_id` int(10) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `faculty_in_charge` text NOT NULL,
  `number_of_people` int(100) NOT NULL,
  `reservation_date` datetime NOT NULL,
  `purpose` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `schedule`
--

INSERT INTO `schedule` (`schedule_id`, `reservation_id`, `user_id`, `firstname`, `lastname`, `email`, `faculty_in_charge`, `number_of_people`, `reservation_date`, `purpose`) VALUES
(1, 2, 3, 'Alice', 'Johnson', 'alice.johnson@example.com', 'James', 5, '2024-03-29 06:11:48', 'Special Exam'),
(2, 1, 1, 'John', 'Doe', 'john.doe@example.com', 'hakdog', 12, '2024-03-06 13:06:39', 'Meeting');

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `user_id` int(10) NOT NULL,
  `student_id` bigint(12) NOT NULL,
  `firstname` text NOT NULL,
  `lastname` text NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`user_id`, `student_id`, `firstname`, `lastname`, `email`, `password`) VALUES
(1, 0, 'John', 'Doe', 'john.doe@example.com', ''),
(2, 0, 'Jane', 'Smith', 'jane.smith@example.com', ''),
(3, 0, 'Alice', 'Johnson', 'alice.johnson@example.com', ''),
(4, 0, 'Bob', 'Williams', 'bob.williams@example.com', ''),
(5, 0, 'Eva', 'Brown', 'eva.brown@example.com', '');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`admin_ID`);

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`history_id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`report_id`);

--
-- Indexes for table `reservation`
--
ALTER TABLE `reservation`
  ADD PRIMARY KEY (`reservation_id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `schedule`
--
ALTER TABLE `schedule`
  ADD PRIMARY KEY (`schedule_id`),
  ADD KEY `reservation_id` (`reservation_id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`user_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reservation`
--
ALTER TABLE `reservation`
  ADD CONSTRAINT `reservation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`);

--
-- Constraints for table `schedule`
--
ALTER TABLE `schedule`
  ADD CONSTRAINT `schedule_ibfk_3` FOREIGN KEY (`reservation_id`) REFERENCES `reservation` (`reservation_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
