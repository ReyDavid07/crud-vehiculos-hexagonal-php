<?php
declare(strict_types=1);
interface GetVehiculoByIdUseCase { public function execute(GetVehiculoByIdQuery $query): VehiculoModel; }
