<?php
require_once 'config.php';
require_once 'functions.php';

$mensaje = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre = limpiar($_POST['nombre'] ?? '');
    $email = limpiar($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    if (strlen($password) < 4) {
        $mensaje = 'La contraseña debe tener al menos 4 caracteres.';
    } else {
        $stmt = $mysqli->prepare('SELECT id FROM users WHERE email = ? LIMIT 1');
        $stmt->bind_param('s', $email);
        $stmt->execute();
        $existe = $stmt->get_result()->fetch_assoc();

        if ($existe) {
            $mensaje = 'Ese email ya está registrado.';
        } else {
            $hash = password_hash($password, PASSWORD_DEFAULT);
            $stmt = $mysqli->prepare('INSERT INTO users (nombre, email, password) VALUES (?, ?, ?)');
            $stmt->bind_param('sss', $nombre, $email, $hash);

            if ($stmt->execute()) {
                header('Location: login.php');
                exit;
            }

            $mensaje = 'No se pudo registrar el usuario.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registro</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container small">
    <h2>Crear cuenta</h2>
    <?php if ($mensaje): ?>
        <p class="alert"><?php echo $mensaje; ?></p>
    <?php endif; ?>

    <form method="POST">
        <label>Nombre</label>
        <input type="text" name="nombre" required>

        <label>Email</label>
        <input type="email" name="email" required>

        <label>Contraseña</label>
        <input type="password" name="password" required>

        <button type="submit" class="btn">Registrarme</button>
    </form>

    <p>¿Ya tienes cuenta? <a href="login.php">Inicia sesión</a></p>
    <p><a href="index.php">Volver al inicio</a></p>
</div>
</body>
</html>
