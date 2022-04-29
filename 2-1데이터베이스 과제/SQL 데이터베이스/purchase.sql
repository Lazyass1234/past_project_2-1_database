-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- 생성 시간: 20-06-23 14:58
-- 서버 버전: 10.4.11-MariaDB
-- PHP 버전: 7.2.31

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `testdb`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `purchase`
--

CREATE TABLE `purchase` (
  `PurchaseCode` int(30) NOT NULL,
  `PurchasedProductCode` int(30) NOT NULL,
  `NameOfPurchasedProducts` text NOT NULL,
  `VolumeOfPurchase` int(255) NOT NULL,
  `InVoiceNumber` int(30) NOT NULL,
  `LumpSum` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 테이블의 덤프 데이터 `purchase`
--

INSERT INTO `purchase` (`PurchaseCode`, `PurchasedProductCode`, `NameOfPurchasedProducts`, `VolumeOfPurchase`, `InVoiceNumber`, `LumpSum`) VALUES
(2131, 1231, '5434', 2131, 12312, 12313),
(122222, 133334, '', 12345, 0, 33231),
(1331454, 133334, '', 12345, 0, 33231),
(1331455, 133334, '', 12345, 0, 33231),
(1331456, 133334, '', 12345, 0, 33231);

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `purchase`
--
ALTER TABLE `purchase`
  ADD PRIMARY KEY (`PurchaseCode`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
