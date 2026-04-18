<?php
class VehiculoNumero
{
    private int $value;
    public function __construct($value, string $field) { if (!is_numeric($value) || (int) $value < 0) { throw InvalidVehiculoNumeroException::becauseValueIsInvalid($field); } $this->value = (int) $value; }
    public function value(): int { return $this->value; }
}
