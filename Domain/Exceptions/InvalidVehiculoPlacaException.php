<?php
class InvalidVehiculoPlacaException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('La placa no puede estar vacía.'); } public static function becauseFormatIsInvalid($value){ return new self('La placa no es válida: '. $value); } }
