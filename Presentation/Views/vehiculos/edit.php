<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Editar vehículo</h2><form method="post" action="index.php?route=vehiculos.update"><input type="hidden" name="id" value="<?= htmlspecialchars($vehiculo->id()->value()) ?>">
<div class="grid">
<div><label>Placa</label><input name="placa" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->placa()->value()) : '' ?>" required></div>
<div><label>Marca</label><input name="marca" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->marca()->value()) : '' ?>" required></div>
<div><label>Modelo</label><input name="modelo" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->modelo()->value()) : '' ?>" required></div>
<div><label>Versión</label><input name="version" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->version()->value()) : '' ?>" required></div>
<div><label>Color</label><input name="color" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->color()->value()) : '' ?>" required></div>
<div><label>Número de puestos</label><input type="number" min="1" name="numPuestos" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->numPuestos()->value()) : '' ?>" required></div>
<div><label>Número de puertas</label><input type="number" min="1" name="numPuertas" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->numPuertas()->value()) : '' ?>" required></div>
<div><label>Combustible</label><input name="combustible" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->combustible()->value()) : '' ?>" required></div>
<div><label>Kilómetros</label><input type="number" min="0" name="kilometros" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->kilometros()->value()) : '' ?>" required></div>
<div><label>Cilindraje</label><input type="number" min="0" name="cilindraje" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->cilindraje()->value()) : '' ?>" required></div>
<div><label>Categoría</label><input name="categoria" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->categoria()->value()) : '' ?>" required></div>
</div>
<button type="submit">Actualizar</button></form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
