<?php
declare(strict_types=1);
interface CreateVehiculoUseCase { public function execute(CreateVehiculoCommand $command): VehiculoModel; }
