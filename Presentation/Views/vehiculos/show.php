<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Detalle de vehículo</h2>
<p><strong>ID:</strong> <?= htmlspecialchars($vehiculo->id()->value()) ?></p>
<p><strong>Placa:</strong> <?= htmlspecialchars($vehiculo->placa()->value()) ?></p>
<p><strong>Marca:</strong> <?= htmlspecialchars($vehiculo->marca()->value()) ?></p>
<p><strong>Modelo:</strong> <?= htmlspecialchars($vehiculo->modelo()->value()) ?></p>
<p><strong>Versión:</strong> <?= htmlspecialchars($vehiculo->version()->value()) ?></p>
<p><strong>Color:</strong> <?= htmlspecialchars($vehiculo->color()->value()) ?></p>
<p><strong>Puestos:</strong> <?= htmlspecialchars((string) $vehiculo->numPuestos()->value()) ?></p>
<p><strong>Puertas:</strong> <?= htmlspecialchars((string) $vehiculo->numPuertas()->value()) ?></p>
<p><strong>Combustible:</strong> <?= htmlspecialchars($vehiculo->combustible()->value()) ?></p>
<p><strong>Kilómetros:</strong> <?= htmlspecialchars((string) $vehiculo->kilometros()->value()) ?></p>
<p><strong>Cilindraje:</strong> <?= htmlspecialchars((string) $vehiculo->cilindraje()->value()) ?></p>
<p><strong>Categoría:</strong> <?= htmlspecialchars($vehiculo->categoria()->value()) ?></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
