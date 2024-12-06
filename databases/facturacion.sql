-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 06-12-2024 a las 22:04:50
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `facturacion`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id` int(5) NOT NULL,
  `concepto` varchar(50) NOT NULL,
  `precio` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id`, `concepto`, `precio`) VALUES
(10, 'Cerveza Lay negrita X30', 68000),
(11, 'Cerveza Lay X30', 68000),
(12, 'Cerveza poker X30', 68000),
(13, 'Cerveza Clud X30         ', 68000),
(14, 'Bretaña X24', 49000),
(15, 'Ponny 1.5 X30', 32000),
(16, 'Ponny litro X30 ', 55000),
(17, 'Ponny p X30', 55000),
(18, 'Ponny mini X30', 42000),
(19, 'Coca-Cola 1.5 X12', 65000),
(20, 'Coca-Cola p X12', 30000),
(21, 'Coca-Cola 250 X12', 10000),
(22, 'Del valle p X12        ', 18000),
(23, 'Del valle 1.5 X12', 45000),
(24, 'agua vida x20', 13000),
(25, 'Cuatro 1.5 X12', 45000),
(26, 'Premio 1.5 X12', 45000),
(27, 'Postobon 3.0 X6', 40000),
(28, 'Postobon 2.5 X8', 37000),
(29, 'Econolitro X12', 35000),
(30, 'Postobon 250 X12', 10000),
(31, 'Scuas 500 X12', 25000),
(32, 'Gatorade X12', 37000),
(33, 'Cristal 3.1 X4', 18000),
(34, 'Cristal mini X24', 12500),
(35, 'Cristal gas mini X12   ', 7000),
(36, 'Agua saborizada X15', 19000),
(37, 'Speed max X24', 30000),
(38, 'Jugo hit X400 X12', 28000),
(39, 'Jugo hit x250 X12', 20000),
(40, 'Agua inn 5L X4', 18000),
(41, 'Agua cielo X24', 19500),
(42, 'Agua mía X20', 15000),
(43, 'Agua mía gas X20', 16000),
(44, 'Cifru mini X15', 12500),
(45, 'Cifru p X12', 13000),
(46, 'Sip x400 X24', 22500),
(47, 'Sip X250 X24', 18500),
(48, 'Sip caja X24    ', 17500),
(51, 'Fruccy caja X24', 19500),
(52, 'jugito para 200 X20', 3000),
(53, 'agua chuspa pq x15', 2500),
(54, 'Bonbon bun x24', 9000),
(55, 'Menta x100', 7500),
(56, 'Frutica X100  ', 7500),
(57, 'Choco break x30', 8500),
(58, 'Choco break x50', 16000),
(59, 'Max combi x100', 8500),
(60, 'Mini bun X100', 12000),
(61, 'Barrilete x40', 9500),
(62, 'Bonbon bun gomita x24', 31000),
(63, 'Banaba anizada X100', 7500),
(64, 'Porulito X24', 4000),
(65, 'Max Melo X50.     ', 8500),
(66, 'Max coco x100', 12000),
(67, 'Detodito x12', 30000),
(68, 'Choclito X12', 20000),
(69, 'Chestri X12', 20000),
(70, 'Dorito X10', 18000),
(71, 'Boliqueso X12', 14000),
(72, 'Rozada X12', 18500),
(73, 'Popeta X6', 11000),
(74, 'Mani moto x12.       ', 17500),
(75, 'Detodito familiar X1', 7200),
(76, 'Rizada familia X1', 6200),
(77, 'Choclito familia X1', 7200),
(78, 'Dorito familia X1         ', 7200),
(79, 'Boliqueso familia X1     ', 6200),
(80, 'Paleta artesanal pq X24     ', 6000),
(81, 'Paleta artesanal gd X12', 6000),
(82, 'Paleta de Chavo x12    ', 6000),
(83, 'Candy surra x50      ', 8000),
(84, 'Candy Ra x30     ', 9000),
(85, 'Caja de ruliz x17', 22000),
(86, 'Caja de ruliz x17   ', 9000),
(87, 'Papa rulas x12', 9000),
(88, 'Tozimiel  x12  ', 9000),
(89, 'Rizada  x12  ', 18500),
(90, 'Papita  x24   ', 6300),
(91, 'Boliqueso x24   ', 6300),
(92, 'Plátano gd x 12  ', 13000),
(93, 'Plátano pq x24 ', 6300),
(94, 'Picadita x24  ', 6300),
(95, 'Torta x17  ', 13500),
(96, 'Tostada pan valle x12  ', 17500),
(97, 'Crocanacho  x12  ', 8500),
(98, 'Polvorosa  x60', 4500),
(99, 'Cuca gd  x12  ', 5000),
(100, 'Cubana gd  x12  ', 5000),
(101, 'Cuca pq  x24  ', 4300),
(102, 'Cubana pq  x24', 4300),
(103, 'Cubana pq x24 ', 4300),
(104, 'Maní tira x20  ', 5000),
(105, 'Gelatina FRUTA x20   ', 10000),
(106, 'Dulce de guayaba X60. ', 24000),
(107, 'Pamelita  x50     ', 6500),
(108, 'Cigarrillo Dulce x80   ', 6500),
(109, 'Empanadita x50     ', 8000),
(110, 'Boloncho  X30  ', 9500),
(111, 'Caramelos duros x100  ', 8000),
(112, 'Almendra  x100  ', 9000),
(113, 'Bola sandía  x60 ', 10000),
(114, 'Bola mango  x60  ', 10000),
(115, 'Bola chicle  x60  ', 10000),
(116, 'Bola  picante x60', 10000),
(117, 'Cocaita x50  ', 8000),
(118, 'Coquito x100  ', 9000),
(119, 'Mallita  x15 ', 7500),
(120, 'Juanchi queso x12', 11000),
(121, 'Juanchi pollo x12  ', 9000),
(122, 'Juanchi picante x12', 9000),
(123, 'Juanchi natural x12', 9000),
(124, 'Picada shis roja x12', 15500),
(125, '118.	Picada shis azul x12', 15500),
(126, 'Picada shis verde x12', 15500),
(127, 'Acetaminofen 500g x100', 14000),
(128, 'ibufla x12', 26000),
(129, 'Alka-seltzer x60', 51000),
(130, 'Ampicilina 500g x100', 40000),
(131, 'mentol x12', 19500),
(132, 'ibuprofeno 800g x50', 14000),
(133, 'Bonfies x20', 56000),
(134, 'Advil max x40', 73000),
(135, 'Noraver noche x6', 18000),
(136, 'Tarrito rojo x8', 14000),
(137, 'Cepillo colgate x12', 26000),
(138, 'arroz', 3000),
(139, 'papa familiar x400gr', 12500);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=140;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
