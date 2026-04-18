<?php
class InvalidVehiculoTextoException extends InvalidArgumentException { public static function becauseValueIsEmpty($field){ return new self('El campo '. $field .' no puede estar vacío.'); } }
