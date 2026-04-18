<?php
class VehiculoAlreadyExistsException extends DomainException { public static function becausePlacaAlreadyExists($placa){ return new self('Ya existe un vehículo con la placa: '. $placa); } }
