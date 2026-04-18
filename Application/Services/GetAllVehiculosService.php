<?php
declare(strict_types=1);
final class GetAllVehiculosService implements GetAllVehiculosUseCase { private GetAllVehiculosPort $port; public function __construct(GetAllVehiculosPort $port){$this->port=$port;} public function execute(GetAllVehiculosQuery $query): array { return $this->port->getAll(); } }
