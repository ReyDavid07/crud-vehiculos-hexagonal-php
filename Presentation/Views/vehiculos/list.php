<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Vehículos</h2><p><a href="index.php?route=vehiculos.create">Crear vehículo</a></p>
<table><thead><tr><th>Placa</th><th>Marca</th><th>Modelo</th><th>Categoría</th><th>Color</th><th>Acciones</th></tr></thead><tbody>
<?php foreach ($vehiculos as $vehiculo): ?>
<tr>
<td><?= htmlspecialchars($vehiculo->placa()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->marca()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->modelo()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->categoria()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->color()->value()) ?></td>
<td>
<a href="index.php?route=vehiculos.show&id=<?= urlencode($vehiculo->id()->value()) ?>">Ver</a> |
<a href="index.php?route=vehiculos.edit&id=<?= urlencode($vehiculo->id()->value()) ?>">Editar</a> |
<form class="inline" method="post" action="index.php?route=vehiculos.delete"><input type="hidden" name="id" value="<?= htmlspecialchars($vehiculo->id()->value()) ?>"><button type="submit">Eliminar</button></form>
</td></tr>
<?php endforeach; ?>
</tbody></table></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
