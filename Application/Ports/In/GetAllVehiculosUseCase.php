<?php
declare(strict_types=1);
interface GetAllVehiculosUseCase { public function execute(GetAllVehiculosQuery $query): array; }
