<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>CRUD Hexagonal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
        header, nav, main { padding: 16px; }
        header { background: #222; color: white; }
        nav { background: #eee; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
        a { color: #0a58ca; text-decoration: none; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align:left; }
        form.inline { display:inline; }
        .container { max-width: 1100px; margin: 0 auto; }
        .card { background:white; padding:16px; margin:16px 0; }
        .flash-success { background:#d1e7dd; padding:10px; margin:12px 0; }
        .flash-error { background:#f8d7da; padding:10px; margin:12px 0; }
        input, select { width:100%; padding:8px; margin:6px 0 12px; }
        button { padding:8px 14px; }
        .grid { display:grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    </style>
</head>
<body>
<header><div class="container"><h1>CRUD Hexagonal PHP + MySQL</h1></div></header>
<nav><div class="container">
    <a href="index.php?route=home">Inicio</a>
    <?php if (isset($_SESSION['auth']['id'])): ?>
        <a href="index.php?route=users.index">Usuarios</a>
        <a href="index.php?route=vehiculos.index">Vehículos</a>
        <span>Sesión: <?= htmlspecialchars($_SESSION['auth']['name']) ?></span>
        <form class="inline" method="post" action="index.php?route=auth.logout"><button type="submit">Salir</button></form>
    <?php else: ?>
        <a href="index.php?route=auth.login">Iniciar sesión</a>
    <?php endif; ?>
</div></nav>
<main><div class="container">
<?php foreach ($flash as $type => $message): ?>
    <div class="flash-<?= htmlspecialchars($type) ?>"><?= htmlspecialchars($message) ?></div>
<?php endforeach; ?>
