<?php
require_once 'config.php';
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hosting - Inicio</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container center">
    <h1>Configurador de Hosting</h1>
    <p>Proyecto simple en PHP + MySQL para registrar usuarios y configurar servidores.</p>

    <?php if (isset($_SESSION['usuario_id'])): ?>
        <a class="btn" href="dashboard.php">Ir al panel</a>
        <a class="btn secondary" href="login.php?logout=1">Cerrar sesión</a>
    <?php else: ?>
        <a class="btn" href="login.php">Iniciar sesión</a>
        <a class="btn secondary" href="register.php">Registrarse</a>
    <?php endif; ?>
</div>
</body>
</html>
