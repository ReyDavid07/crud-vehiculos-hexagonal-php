<?php
declare(strict_types=1);
interface GetVehiculoByIdPort { public function getById(VehiculoId $vehiculoId): ?VehiculoModel; }
