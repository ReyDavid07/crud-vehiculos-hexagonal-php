<?php
class InvalidVehiculoNumeroException extends InvalidArgumentException { public static function becauseValueIsInvalid($field){ return new self('El campo '. $field .' debe ser un número válido mayor o igual a cero.'); } }
