<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Usuarios</h2><p><a href="index.php?route=users.create">Crear usuario</a></p>
<table><thead><tr><th>Nombre</th><th>Email</th><th>Rol</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>
<?php foreach ($users as $user): ?>
<tr>
<td><?= htmlspecialchars($user->name()->value()) ?></td>
<td><?= htmlspecialchars($user->email()->value()) ?></td>
<td><?= htmlspecialchars($user->role()) ?></td>
<td><?= htmlspecialchars($user->status()) ?></td>
<td>
<a href="index.php?route=users.show&id=<?= urlencode($user->id()->value()) ?>">Ver</a> |
<a href="index.php?route=users.edit&id=<?= urlencode($user->id()->value()) ?>">Editar</a> |
<form class="inline" method="post" action="index.php?route=users.delete"><input type="hidden" name="id" value="<?= htmlspecialchars($user->id()->value()) ?>"><button type="submit">Eliminar</button></form>
</td></tr>
<?php endforeach; ?>
</tbody></table></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
