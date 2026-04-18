<?php
class InvalidVehiculoIdException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('El ID del vehículo no puede estar vacío.'); } }
