<?php
function limpiar($valor)
{
    return htmlspecialchars(trim($valor), ENT_QUOTES, 'UTF-8');
}

function usuarioLogueado()
{
    return isset($_SESSION['usuario_id']);
}

function redirigirSiNoLogueado()
{
    if (!usuarioLogueado()) {
        header('Location: login.php');
        exit;
    }
}

function calcularPrecio(array $datos)
{
    $vcpu = max(1, (int)$datos['vcpu']);
    $ram = max(1, (int)$datos['ram']);
    $ssd = max(0, (int)$datos['ssd']);
    $hdd = max(0, (int)$datos['hdd']);
    $bandwidth = max(100, (int)$datos['bandwidth']);

    $base = 0;
    $base += $vcpu * 4;
    $base += $ram * 2.5;
    $base += $ssd * 0.08;
    $base += $hdd * 0.025;
    $base += ($bandwidth / 100) * 2;

    if (!empty($datos['windows_server'])) {
        $base += 15;
    }
    if (!empty($datos['ip_estatica'])) {
        $base += 3;
    }
    if (!empty($datos['firewall'])) {
        $base += 2;
    }
    if (!empty($datos['panel_control'])) {
        $base += 12;
    }

    $backup = !empty($datos['backup']) ? $base * 0.20 : 0;
    $total = $base + $backup;

    return [
        'base' => round($base, 2),
        'backup' => round($backup, 2),
        'total' => round($total, 2)
    ];
}
?>
