<?php
declare(strict_types=1);
interface DeleteVehiculoUseCase { public function execute(DeleteVehiculoCommand $command): void; }
