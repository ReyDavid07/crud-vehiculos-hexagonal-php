<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card">
    <h2>Recuperar contraseña</h2>
    <form method="post" action="index.php?route=auth.sendForgot">
        <label>Correo</label><input type="email" name="email" required>
        <button type="submit">Enviar contraseña temporal</button>
    </form>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
