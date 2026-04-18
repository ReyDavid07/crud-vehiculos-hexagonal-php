<?php
declare(strict_types=1);
final class Flash
{
    public static function set(string $key, string $message): void { $_SESSION['_flash'][$key] = $message; }
    public static function all(): array { $flash = $_SESSION['_flash'] ?? []; unset($_SESSION['_flash']); return $flash; }
}
