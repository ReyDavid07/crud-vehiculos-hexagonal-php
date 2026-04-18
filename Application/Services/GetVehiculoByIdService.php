<?php
declare(strict_types=1);
final class GetVehiculoByIdService implements GetVehiculoByIdUseCase { private GetVehiculoByIdPort $port; public function __construct(GetVehiculoByIdPort $port){$this->port=$port;} public function execute(GetVehiculoByIdQuery $query): VehiculoModel { $id = VehiculoApplicationMapper::fromGetVehiculoByIdQueryToVehiculoId($query); $vehiculo = $this->port->getById($id); if ($vehiculo===null){ throw VehiculoNotFoundException::becauseIdWasNotFound($id->value()); } return $vehiculo; } }
