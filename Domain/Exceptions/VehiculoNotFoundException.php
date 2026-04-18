<?php
class VehiculoNotFoundException extends DomainException { public static function becauseIdWasNotFound($id){ return new self('No se encontró un vehículo con el ID: '. $id); } }
