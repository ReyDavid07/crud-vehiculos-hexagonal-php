<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card">
    <h2>Iniciar sesión</h2>
    <form method="post" action="index.php?route=auth.authenticate">
        <label>Correo</label><input type="email" name="email" required>
        <label>Contraseña</label><input type="password" name="password" required>
        <button type="submit">Ingresar</button>
    </form>
    <p><a href="index.php?route=auth.forgot">¿Olvidaste tu contraseña?</a></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
