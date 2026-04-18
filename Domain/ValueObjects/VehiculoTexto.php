<?php
class VehiculoTexto
{
    private string $value;
    public function __construct($value, string $field) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidVehiculoTextoException::becauseValueIsEmpty($field); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
}
