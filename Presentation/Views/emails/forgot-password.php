<!doctype html>
<html lang="es"><body>
<h2>Recuperación de contraseña</h2>
<p>Hola <?= htmlspecialchars($name) ?>,</p>
<p>Se ha generado una contraseña temporal para tu cuenta <?= htmlspecialchars($email) ?>.</p>
<p><strong>Contraseña temporal:</strong> <?= htmlspecialchars($temporaryPassword) ?></p>
<p>Inicia sesión y luego cambia la contraseña desde el módulo de usuarios.</p>
</body></html>
