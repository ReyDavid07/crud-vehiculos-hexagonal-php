<?php
class UserEmail
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserEmailException::becauseValueIsEmpty(); } if (!filter_var($normalized, FILTER_VALIDATE_EMAIL)) { throw InvalidUserEmailException::becauseFormatIsInvalid($normalized); } $this->value = strtolower($normalized); }
    public function value(): string { return $this->value; }
    public function equals(UserEmail $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
