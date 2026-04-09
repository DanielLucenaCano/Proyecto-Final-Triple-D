<?php
require_once 'config.php';
require_once 'functions.php';

redirigirSiNoLogueado();

$mensaje = '';
$precio = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['crear_servidor'])) {
    $nombreServidor = limpiar($_POST['nombre_servidor'] ?? 'Servidor sin nombre');

    $datos = [
        'vcpu' => $_POST['vcpu'] ?? 1,
        'ram' => $_POST['ram'] ?? 1,
        'ssd' => $_POST['ssd'] ?? 0,
        'hdd' => $_POST['hdd'] ?? 0,
        'bandwidth' => $_POST['bandwidth'] ?? 100,
        'windows_server' => isset($_POST['windows_server']) ? 1 : 0,
        'ip_estatica' => isset($_POST['ip_estatica']) ? 1 : 0,
        'backup' => isset($_POST['backup']) ? 1 : 0,
        'firewall' => isset($_POST['firewall']) ? 1 : 0,
        'panel_control' => isset($_POST['panel_control']) ? 1 : 0,
    ];

    $precio = calcularPrecio($datos);

    $stmt = $mysqli->prepare('INSERT INTO servers (user_id, nombre, vcpu, ram, ssd, hdd, bandwidth, windows_server, ip_estatica, backup, firewall, panel_control, precio_base, precio_total, estado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)');
    $estado = 'detenido';
    $stmt->bind_param(
        'isiiiiiiiiiiids',
        $_SESSION['usuario_id'],
        $nombreServidor,
        $datos['vcpu'],
        $datos['ram'],
        $datos['ssd'],
        $datos['hdd'],
        $datos['bandwidth'],
        $datos['windows_server'],
        $datos['ip_estatica'],
        $datos['backup'],
        $datos['firewall'],
        $datos['panel_control'],
        $precio['base'],
        $precio['total'],
        $estado
    );

    if ($stmt->execute()) {
        $mensaje = 'Servidor creado correctamente.';
    } else {
        $mensaje = 'Error al crear el servidor.';
    }
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion_estado'])) {
    $serverId = (int)$_POST['server_id'];
    $accion = $_POST['accion_estado'] === 'iniciar' ? 'activo' : 'detenido';

    $stmt = $mysqli->prepare('UPDATE servers SET estado = ? WHERE id = ? AND user_id = ?');
    $stmt->bind_param('sii', $accion, $serverId, $_SESSION['usuario_id']);
    $stmt->execute();
}

$stmt = $mysqli->prepare('SELECT * FROM servers WHERE user_id = ? ORDER BY id DESC');
$stmt->bind_param('i', $_SESSION['usuario_id']);
$stmt->execute();
$servidores = $stmt->get_result();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
<div class="container">
    <div class="header-row">
        <h2>Bienvenido, <?php echo htmlspecialchars($_SESSION['usuario_nombre']); ?></h2>
        <a class="btn secondary" href="login.php?logout=1">Cerrar sesión</a>
    </div>

    <?php if ($mensaje): ?>
        <p class="success"><?php echo $mensaje; ?></p>
    <?php endif; ?>

    <h3>Nuevo servidor</h3>
    <form method="POST" id="form-configuracion">
        <input type="hidden" name="crear_servidor" value="1">

        <label>Nombre del servidor</label>
        <input type="text" name="nombre_servidor" required>

        <div class="grid">
            <div>
                <label>vCPU</label>
                <input type="number" name="vcpu" min="1" value="2" required>
            </div>
            <div>
                <label>RAM (GB)</label>
                <input type="number" name="ram" min="1" value="4" required>
            </div>
            <div>
                <label>SSD (GB)</label>
                <input type="number" name="ssd" min="0" value="80">
            </div>
            <div>
                <label>HDD (GB)</label>
                <input type="number" name="hdd" min="0" value="0">
            </div>
            <div>
                <label>Ancho de banda (Mbps)</label>
                <input type="number" name="bandwidth" min="100" step="100" value="100">
            </div>
        </div>

        <div class="checks">
            <label><input type="checkbox" name="windows_server"> Windows Server (+15€)</label>
            <label><input type="checkbox" name="ip_estatica"> IP estática (+3€)</label>
            <label><input type="checkbox" name="backup"> Backup (+20% base)</label>
            <label><input type="checkbox" name="firewall"> Firewall (+2€)</label>
            <label><input type="checkbox" name="panel_control"> Panel de control (+12€)</label>
        </div>

        <p id="precio_estimado">Precio estimado: <strong>0.00€</strong></p>
        <button class="btn" type="submit">Guardar servidor</button>
    </form>

    <h3>Mis servidores</h3>
    <table>
        <thead>
        <tr>
            <th>Nombre</th>
            <th>Recursos</th>
            <th>Precio mensual</th>
            <th>Estado</th>
            <th>Acciones</th>
        </tr>
        </thead>
        <tbody>
        <?php while ($srv = $servidores->fetch_assoc()): ?>
            <tr>
                <td><?php echo htmlspecialchars($srv['nombre']); ?></td>
                <td>
                    <?php echo (int)$srv['vcpu']; ?> vCPU,
                    <?php echo (int)$srv['ram']; ?>GB RAM,
                    <?php echo (int)$srv['ssd']; ?>GB SSD,
                    <?php echo (int)$srv['hdd']; ?>GB HDD
                </td>
                <td><?php echo number_format((float)$srv['precio_total'], 2); ?>€</td>
                <td>
                    <span class="badge <?php echo $srv['estado'] === 'activo' ? 'on' : 'off'; ?>">
                        <?php echo htmlspecialchars($srv['estado']); ?>
                    </span>
                </td>
                <td>
                    <form method="POST" class="inline">
                        <input type="hidden" name="server_id" value="<?php echo (int)$srv['id']; ?>">
                        <?php if ($srv['estado'] === 'detenido'): ?>
                            <button class="btn mini" name="accion_estado" value="iniciar" type="submit">Iniciar</button>
                        <?php else: ?>
                            <button class="btn mini danger" name="accion_estado" value="detener" type="submit">Detener</button>
                        <?php endif; ?>
                    </form>
                </td>
            </tr>
        <?php endwhile; ?>
        </tbody>
    </table>
</div>
<script src="script.js"></script>
</body>
</html>
