<?php
declare(strict_types=1);
interface GetVehiculoByPlacaPort { public function getByPlaca(VehiculoPlaca $placa): ?VehiculoModel; }
