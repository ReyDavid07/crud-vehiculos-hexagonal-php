<?php
declare(strict_types=1);

final class ClassLoader
{
    public static function register(string $projectRoot): void
    {
        spl_autoload_register(function (string $className) use ($projectRoot): void {
            $iterator = new RecursiveIteratorIterator(
                new RecursiveDirectoryIterator($projectRoot, FilesystemIterator::SKIP_DOTS)
            );

            foreach ($iterator as $file) {
                if (!$file->isFile() || $file->getExtension() !== 'php') {
                    continue;
                }

                if ($file->getBasename('.php') === $className) {
                    require_once $file->getPathname();
                    return;
                }
            }
        });
    }
}
