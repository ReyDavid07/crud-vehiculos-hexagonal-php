<?php
class UserRoleEnum
{
    public const ADMIN = 'ADMIN';
    public const MEMBER = 'MEMBER';
    public const REVIEWER = 'REVIEWER';
    public static function values(): array { return [self::ADMIN, self::MEMBER, self::REVIEWER]; }
    public static function isValid(string $value): bool { return in_array($value, self::values(), true); }
    public static function ensureIsValid(string $value): void { if (!self::isValid($value)) { throw InvalidUserRoleException::becauseValueIsInvalid($value); } }
}
