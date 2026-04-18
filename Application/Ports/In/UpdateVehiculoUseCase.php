<?php
declare(strict_types=1);
interface UpdateVehiculoUseCase { public function execute(UpdateVehiculoCommand $command): VehiculoModel; }
