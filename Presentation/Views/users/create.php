<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Crear usuario</h2><form method="post" action="index.php?route=users.store">
<label>Nombre</label><input name="name" required>
<label>Email</label><input type="email" name="email" required>
<label>Contraseña</label><input type="password" name="password" required>
<label>Rol</label><select name="role"><option>ADMIN</option><option selected>MEMBER</option><option>REVIEWER</option></select>
<button type="submit">Guardar</button>
</form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
