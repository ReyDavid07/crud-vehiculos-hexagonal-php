<?php
class UserId
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserIdException::becauseValueIsEmpty(); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(UserId $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
