-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 05-12-2025 a las 21:22:03
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
-- Base de datos: `db_parqueo`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `parqueadero`
--

CREATE TABLE `parqueadero` (
  `nit` varchar(15) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(150) NOT NULL,
  `departamento` varchar(50) NOT NULL,
  `ciudad` varchar(50) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `correo` varchar(80) DEFAULT NULL,
  `fecha_registro` date DEFAULT curdate(),
  `estado` enum('activo','inactivo') DEFAULT 'activo',
  `capacidad_carros` int(11) DEFAULT 0,
  `capacidad_motos` int(11) DEFAULT 0,
  `operaciones_carro` int(11) DEFAULT 0,
  `operaciones_moto` int(11) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `parqueadero`
--

INSERT INTO `parqueadero` (`nit`, `nombre`, `direccion`, `departamento`, `ciudad`, `telefono`, `correo`, `fecha_registro`, `estado`, `capacidad_carros`, `capacidad_motos`, `operaciones_carro`, `operaciones_moto`) VALUES
('0001', 'Parkings Stark', 'Calle Malibu Point #10880', 'California', 'Malibu', '3120987654', 'stark@mail.com', '2025-10-23', 'activo', 1, 1, 0, 0);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `registros`
--

CREATE TABLE `registros` (
  `id_registros` int(11) NOT NULL,
  `parqueadero_nit` varchar(15) DEFAULT NULL,
  `usuario_cedula` varchar(15) DEFAULT NULL,
  `vehiculo_placa` varchar(7) DEFAULT NULL,
  `fecha_ingreso` datetime DEFAULT NULL,
  `fecha_salida` datetime DEFAULT NULL,
  `tarifa_id` int(11) DEFAULT NULL,
  `total` decimal(10,2) DEFAULT NULL,
  `activo` enum('activo','inactivo') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tarifas`
--

CREATE TABLE `tarifas` (
  `id_tarifas` int(11) NOT NULL,
  `parqueadero_nit` varchar(15) DEFAULT NULL,
  `tipo_tarifa` enum('primera_hora','hora_extra','jornada','dia_completo') NOT NULL,
  `horario` enum('diurno','nocturno') NOT NULL,
  `tipo_vehiculo` enum('carro','moto') DEFAULT NULL,
  `valor_tarifa` int(6) DEFAULT NULL,
  `hora_inicio` time DEFAULT NULL,
  `hora_fin` time DEFAULT NULL,
  `activo` enum('activo','inactivo') DEFAULT 'activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `tarifas`
--

INSERT INTO `tarifas` (`id_tarifas`, `parqueadero_nit`, `tipo_tarifa`, `horario`, `tipo_vehiculo`, `valor_tarifa`, `hora_inicio`, `hora_fin`, `activo`) VALUES
(1, '0001', 'primera_hora', 'diurno', 'moto', 5000, '08:00:00', '17:59:00', 'inactivo'),
(2, '0001', 'hora_extra', 'diurno', 'moto', 1000, '20:00:00', '17:59:00', 'inactivo'),
(3, '0001', 'jornada', 'diurno', 'carro', 10000, '08:00:00', '19:59:00', 'inactivo'),
(4, '0001', 'dia_completo', 'nocturno', 'moto', 25000, '20:50:00', '12:50:00', 'inactivo'),
(5, '0001', 'dia_completo', 'nocturno', 'carro', 2000, '21:52:00', '02:58:00', 'inactivo'),
(6, '0001', 'primera_hora', 'diurno', 'carro', 500, '11:00:00', '00:00:00', 'activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `cedula` varchar(15) NOT NULL,
  `parqueadero_nit` varchar(15) DEFAULT NULL,
  `nombres` varchar(60) DEFAULT NULL,
  `apellidos` varchar(60) DEFAULT NULL,
  `correo` varchar(80) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `tel_emergencia` varchar(20) DEFAULT NULL,
  `rol` enum('admin','portero','cliente') DEFAULT NULL,
  `activo` enum('activo','inactivo') DEFAULT 'activo',
  `fecha_registro` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`cedula`, `parqueadero_nit`, `nombres`, `apellidos`, `correo`, `telefono`, `tel_emergencia`, `rol`, `activo`, `fecha_registro`) VALUES
('1234567890', '0001', 'Emily', 'Stark', 'e@mail.com', '3120000000', '3111111111', 'admin', 'activo', '2025-10-23 00:00:00');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `parqueadero`
--
ALTER TABLE `parqueadero`
  ADD PRIMARY KEY (`nit`);

--
-- Indices de la tabla `registros`
--
ALTER TABLE `registros`
  ADD PRIMARY KEY (`id_registros`),
  ADD KEY `parqueadero_nit` (`parqueadero_nit`),
  ADD KEY `usuario_cedula` (`usuario_cedula`),
  ADD KEY `vehiculo_placa` (`vehiculo_placa`),
  ADD KEY `tarifa_id` (`tarifa_id`);

--
-- Indices de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD PRIMARY KEY (`id_tarifas`),
  ADD KEY `parqueadero_nit` (`parqueadero_nit`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`cedula`),
  ADD KEY `parqueadero_nit` (`parqueadero_nit`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `registros`
--
ALTER TABLE `registros`
  MODIFY `id_registros` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tarifas`
--
ALTER TABLE `tarifas`
  MODIFY `id_tarifas` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `registros`
--
ALTER TABLE `registros`
  ADD CONSTRAINT `fk_registros_parqueadero` FOREIGN KEY (`parqueadero_nit`) REFERENCES `parqueadero` (`nit`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_registros_tarifa` FOREIGN KEY (`tarifa_id`) REFERENCES `tarifas` (`id_tarifas`) ON DELETE SET NULL ON UPDATE CASCADE,
  ADD CONSTRAINT `fk_registros_usuario` FOREIGN KEY (`usuario_cedula`) REFERENCES `usuarios` (`cedula`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `tarifas`
--
ALTER TABLE `tarifas`
  ADD CONSTRAINT `fk_tarifas_parqueadero` FOREIGN KEY (`parqueadero_nit`) REFERENCES `parqueadero` (`nit`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Filtros para la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD CONSTRAINT `fk_usuarios_parqueadero` FOREIGN KEY (`parqueadero_nit`) REFERENCES `parqueadero` (`nit`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
