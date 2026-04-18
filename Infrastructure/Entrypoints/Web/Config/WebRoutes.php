<?php
declare(strict_types=1);
final class WebRoutes
{
    public static function all(): array
    {
        return [
            'home' => ['GET', 'home'],
            'auth.login' => ['GET', 'auth.login'],
            'auth.authenticate' => ['POST', 'auth.authenticate'],
            'auth.logout' => ['POST', 'auth.logout'],
            'auth.forgot' => ['GET', 'auth.forgot'],
            'auth.sendForgot' => ['POST', 'auth.sendForgot'],
            'users.index' => ['GET', 'users.index'],
            'users.create' => ['GET', 'users.create'],
            'users.store' => ['POST', 'users.store'],
            'users.show' => ['GET', 'users.show'],
            'users.edit' => ['GET', 'users.edit'],
            'users.update' => ['POST', 'users.update'],
            'users.delete' => ['POST', 'users.delete'],
            'vehiculos.index' => ['GET', 'vehiculos.index'],
            'vehiculos.create' => ['GET', 'vehiculos.create'],
            'vehiculos.store' => ['POST', 'vehiculos.store'],
            'vehiculos.show' => ['GET', 'vehiculos.show'],
            'vehiculos.edit' => ['GET', 'vehiculos.edit'],
            'vehiculos.update' => ['POST', 'vehiculos.update'],
            'vehiculos.delete' => ['POST', 'vehiculos.delete'],
        ];
    }
}
