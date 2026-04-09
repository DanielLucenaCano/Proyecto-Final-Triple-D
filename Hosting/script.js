(function () {
    var form = document.getElementById('form-configuracion');
    if (!form) return;

    var salida = document.getElementById('precio_estimado');

    function numero(name, min) {
        var input = form.querySelector('[name="' + name + '"]');
        var value = parseFloat(input.value) || 0;
        return Math.max(min, value);
    }

    function marcado(name) {
        var input = form.querySelector('[name="' + name + '"]');
        return input ? input.checked : false;
    }

    function calcular() {
        var vcpu = numero('vcpu', 1);
        var ram = numero('ram', 1);
        var ssd = numero('ssd', 0);
        var hdd = numero('hdd', 0);
        var bandwidth = numero('bandwidth', 100);

        var base = 0;
        base += vcpu * 4;
        base += ram * 2.5;
        base += ssd * 0.08;
        base += hdd * 0.025;
        base += (bandwidth / 100) * 2;

        if (marcado('windows_server')) base += 15;
        if (marcado('ip_estatica')) base += 3;
        if (marcado('firewall')) base += 2;
        if (marcado('panel_control')) base += 12;

        var backup = marcado('backup') ? base * 0.20 : 0;
        var total = base + backup;

        salida.innerHTML = 'Precio estimado: <strong>' + total.toFixed(2) + '€</strong>';
    }

    form.addEventListener('input', calcular);
    calcular();
})();
