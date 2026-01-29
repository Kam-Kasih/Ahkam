-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jan 22, 2026 at 03:04 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `rapot_Ahkam`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi_Ahkam`
--

CREATE TABLE `absensi_Ahkam` (
  `id_absen` varchar(100) NOT NULL,
  `nis` int(11) NOT NULL,
  `sakit` int(11) NOT NULL,
  `izin` int(11) NOT NULL,
  `alfa` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `absensi_Ahkam`
--

INSERT INTO `absensi_Ahkam` (`id_absen`, `nis`, `sakit`, `izin`, `alfa`) VALUES
('A001', 10243293, 2, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `guru_Ahkam`
--

CREATE TABLE `guru_Ahkam` (
  `id_guru` varchar(100) NOT NULL,
  `nama_guru` varchar(50) NOT NULL,
  `id_mapel` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `guru_Ahkam`
--

INSERT INTO `guru_Ahkam` (`id_guru`, `nama_guru`, `id_mapel`) VALUES
('G001', 'Joko', 'M001');

-- --------------------------------------------------------

--
-- Table structure for table `kelas_Ahkam`
--

CREATE TABLE `kelas_Ahkam` (
  `id_kelas` varchar(100) NOT NULL,
  `nama_kelas` varchar(50) NOT NULL,
  `id_guru` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas_Ahkam`
--

INSERT INTO `kelas_Ahkam` (`id_kelas`, `nama_kelas`, `id_guru`) VALUES
('K001', 'XI RPL B', 'G001');

-- --------------------------------------------------------

--
-- Table structure for table `mapel_Ahkam`
--

CREATE TABLE `mapel_Ahkam` (
  `id_mapel` varchar(100) NOT NULL,
  `nama_mapel` varchar(50) NOT NULL,
  `kkm` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mapel_Ahkam`
--

INSERT INTO `mapel_Ahkam` (`id_mapel`, `nama_mapel`, `kkm`) VALUES
('M001', 'B.Jepang', 75),
('M002', 'B.Indonesia', 75),
('M003', 'B.Inggris', 80);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_Ahkam`
--

CREATE TABLE `nilai_Ahkam` (
  `id_nilai` varchar(10) NOT NULL,
  `nis` int(11) NOT NULL,
  `id_mapel` varchar(100) NOT NULL,
  `nilai_tugas` int(11) NOT NULL,
  `nilai_uts` int(11) NOT NULL,
  `nilai_uas` int(11) NOT NULL,
  `nilai_akhir` int(11) NOT NULL,
  `deskripsi` varchar(50) NOT NULL,
  `semester` varchar(50) NOT NULL,
  `tahun_ajaran` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nilai_Ahkam`
--

INSERT INTO `nilai_Ahkam` (`id_nilai`, `nis`, `id_mapel`, `nilai_tugas`, `nilai_uts`, `nilai_uas`, `nilai_akhir`, `deskripsi`, `semester`, `tahun_ajaran`) VALUES
('N001', 10243293, 'M001', 80, 90, 89, 86, 'Baguss', '1', 2025),
('N002', 10243293, 'M003', 80, 90, 45, 71, 'lebih giat lagi', '2', 2026);

-- --------------------------------------------------------

--
-- Table structure for table `siswa_Ahkam`
--

CREATE TABLE `siswa_Ahkam` (
  `nis` int(11) NOT NULL,
  `nama` varchar(50) NOT NULL,
  `tempat_lahir` varchar(100) NOT NULL,
  `tgl_lahir` date NOT NULL,
  `alamat` varchar(100) NOT NULL,
  `id_kelas` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `siswa_Ahkam`
--

INSERT INTO `siswa_Ahkam` (`nis`, `nama`, `tempat_lahir`, `tgl_lahir`, `alamat`, `id_kelas`) VALUES
(10243293, 'Ahkam', 'Bekasi', '2009-05-07', 'Jl.Pojok Selatan No 8/56', 'K001');

-- --------------------------------------------------------

--
-- Table structure for table `user_Ahkam`
--

CREATE TABLE `user_Ahkam` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `role` enum('admin','guru','wali kelas') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_Ahkam`
--

INSERT INTO `user_Ahkam` (`id`, `username`, `password`, `role`) VALUES
(12345610, 'Udin', 'Udin123', 'wali kelas'),
(12345678, 'Jann', 'Jann123', 'admin'),
(12345679, 'Billie', 'Billie123', 'guru');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi_Ahkam`
--
ALTER TABLE `absensi_Ahkam`
  ADD PRIMARY KEY (`id_absen`),
  ADD KEY `nis` (`nis`);

--
-- Indexes for table `guru_Ahkam`
--
ALTER TABLE `guru_Ahkam`
  ADD PRIMARY KEY (`id_guru`),
  ADD KEY `id_mapel` (`id_mapel`);

--
-- Indexes for table `kelas_Ahkam`
--
ALTER TABLE `kelas_Ahkam`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `id_guru` (`id_guru`);

--
-- Indexes for table `mapel_Ahkam`
--
ALTER TABLE `mapel_Ahkam`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `nilai_Ahkam`
--
ALTER TABLE `nilai_Ahkam`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `nis` (`nis`,`id_mapel`),
  ADD KEY `nilai_Ahkam_ibfk_1` (`id_mapel`);

--
-- Indexes for table `siswa_Ahkam`
--
ALTER TABLE `siswa_Ahkam`
  ADD PRIMARY KEY (`nis`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- Indexes for table `user_Ahkam`
--
ALTER TABLE `user_Ahkam`
  ADD PRIMARY KEY (`id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi_Ahkam`
--
ALTER TABLE `absensi_Ahkam`
  ADD CONSTRAINT `absensi_Ahkam_ibfk_1` FOREIGN KEY (`nis`) REFERENCES `siswa_Ahkam` (`nis`);

--
-- Constraints for table `guru_Ahkam`
--
ALTER TABLE `guru_Ahkam`
  ADD CONSTRAINT `guru_Ahkam_ibfk_1` FOREIGN KEY (`id_mapel`) REFERENCES `mapel_Ahkam` (`id_mapel`);

--
-- Constraints for table `kelas_Ahkam`
--
ALTER TABLE `kelas_Ahkam`
  ADD CONSTRAINT `kelas_Ahkam_ibfk_1` FOREIGN KEY (`id_guru`) REFERENCES `guru_Ahkam` (`id_guru`);

--
-- Constraints for table `nilai_Ahkam`
--
ALTER TABLE `nilai_Ahkam`
  ADD CONSTRAINT `nilai_Ahkam_ibfk_1` FOREIGN KEY (`id_mapel`) REFERENCES `mapel_Ahkam` (`id_mapel`),
  ADD CONSTRAINT `nilai_Ahkam_ibfk_2` FOREIGN KEY (`nis`) REFERENCES `siswa_Ahkam` (`nis`);

--
-- Constraints for table `siswa_Ahkam`
--
ALTER TABLE `siswa_Ahkam`
  ADD CONSTRAINT `siswa_Ahkam_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas_Ahkam` (`id_kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
