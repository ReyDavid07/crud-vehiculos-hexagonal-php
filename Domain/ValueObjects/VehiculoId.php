<?php
class VehiculoId
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidVehiculoIdException::becauseValueIsEmpty(); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(VehiculoId $other): bool { return $this->value === $other->value(); }
}
