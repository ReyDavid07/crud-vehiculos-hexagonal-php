<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Detalle de usuario</h2>
<p><strong>ID:</strong> <?= htmlspecialchars($user->id()->value()) ?></p>
<p><strong>Nombre:</strong> <?= htmlspecialchars($user->name()->value()) ?></p>
<p><strong>Email:</strong> <?= htmlspecialchars($user->email()->value()) ?></p>
<p><strong>Rol:</strong> <?= htmlspecialchars($user->role()) ?></p>
<p><strong>Estado:</strong> <?= htmlspecialchars($user->status()) ?></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
