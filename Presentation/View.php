<?php
declare(strict_types=1);
final class View
{
    public static function render(string $template, array $data = []): void
    {
        extract($data);
        $flash = Flash::all();
        require dirname(__DIR__) . '/Presentation/Views/' . $template . '.php';
    }
    public static function redirect(string $route): void
    {
        header('Location: index.php?route=' . $route);
        exit;
    }
}
