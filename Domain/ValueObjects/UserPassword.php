<?php
class UserPassword
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserPasswordException::becauseValueIsEmpty(); } if (strlen($normalized) < 8) { throw InvalidUserPasswordException::becauseLengthIsTooShort(8); } $this->value = $normalized; }
    public static function fromPlainText(string $raw): self { $normalized = trim($raw); if ($normalized === '') { throw InvalidUserPasswordException::becauseValueIsEmpty(); } if (strlen($normalized) < 8) { throw InvalidUserPasswordException::becauseLengthIsTooShort(8); } return new self(password_hash($normalized, PASSWORD_BCRYPT)); }
    public static function fromHash(string $hash): self { return new self($hash); }
    public function verifyPlain(string $plain): bool { return password_verify($plain, $this->value); }
    public function value(): string { return $this->value; }
    public function equals(UserPassword $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
