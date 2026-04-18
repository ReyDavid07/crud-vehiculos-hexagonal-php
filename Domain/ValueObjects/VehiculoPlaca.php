<?php
class VehiculoPlaca
{
    private string $value;
    public function __construct($value) { $normalized = strtoupper(trim((string) $value)); if ($normalized === '') { throw InvalidVehiculoPlacaException::becauseValueIsEmpty(); } if (!preg_match('/^[A-Z0-9-]{5,10}$/', $normalized)) { throw InvalidVehiculoPlacaException::becauseFormatIsInvalid($normalized); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(VehiculoPlaca $other): bool { return $this->value === $other->value(); }
}
