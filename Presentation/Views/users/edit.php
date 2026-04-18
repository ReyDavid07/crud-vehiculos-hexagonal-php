<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Editar usuario</h2><form method="post" action="index.php?route=users.update">
<input type="hidden" name="id" value="<?= htmlspecialchars($user->id()->value()) ?>">
<label>Nombre</label><input name="name" value="<?= htmlspecialchars($user->name()->value()) ?>" required>
<label>Email</label><input type="email" name="email" value="<?= htmlspecialchars($user->email()->value()) ?>" required>
<label>Nueva contraseña</label><input type="password" name="password">
<label>Rol</label><select name="role"><?php foreach (UserRoleEnum::values() as $role): ?><option value="<?= htmlspecialchars($role) ?>" <?= $role === $user->role() ? 'selected' : '' ?>><?= htmlspecialchars($role) ?></option><?php endforeach; ?></select>
<label>Estado</label><select name="status"><?php foreach (UserStatusEnum::values() as $status): ?><option value="<?= htmlspecialchars($status) ?>" <?= $status === $user->status() ? 'selected' : '' ?>><?= htmlspecialchars($status) ?></option><?php endforeach; ?></select>
<button type="submit">Actualizar</button>
</form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
