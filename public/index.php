<?php
declare(strict_types=1);

session_start();

$projectRoot = dirname(__DIR__);
require_once $projectRoot . '/Common/DependencyInjection.php';
DependencyInjection::bootstrap($projectRoot);

$route = $_GET['route'] ?? 'home';
$routes = WebRoutes::all();
if (!isset($routes[$route])) {
    http_response_code(404);
    echo 'Ruta no encontrada';
    exit;
}
[$expectedMethod, $action] = $routes[$route];
if ($_SERVER['REQUEST_METHOD'] !== $expectedMethod) {
    http_response_code(405);
    echo 'Método no permitido';
    exit;
}

$publicRoutes = ['home', 'auth.login', 'auth.authenticate', 'auth.forgot', 'auth.sendForgot'];
if (!in_array($route, $publicRoutes, true) && !isset($_SESSION['auth']['id'])) {
    Flash::set('error', 'Debes iniciar sesión.');
    View::redirect('auth.login');
}

try {
    switch ($action) {
        case 'home': View::render('home'); break;
        case 'auth.login': View::render('auth/login'); break;
        case 'auth.forgot': View::render('auth/forgot'); break;
        case 'auth.authenticate': (new AuthController())->authenticate($_POST); break;
        case 'auth.logout': (new AuthController())->logout(); break;
        case 'auth.sendForgot': (new AuthController())->forgot($_POST); break;
        case 'users.index': View::render('users/list', (new UserController())->index()); break;
        case 'users.create': View::render('users/create'); break;
        case 'users.store': (new UserController())->store($_POST); break;
        case 'users.show': View::render('users/show', (new UserController())->show($_GET['id'] ?? '')); break;
        case 'users.edit': View::render('users/edit', (new UserController())->show($_GET['id'] ?? '')); break;
        case 'users.update': (new UserController())->update($_POST); break;
        case 'users.delete': (new UserController())->delete($_POST); break;
        case 'vehiculos.index': View::render('vehiculos/list', (new VehiculoController())->index()); break;
        case 'vehiculos.create': View::render('vehiculos/create'); break;
        case 'vehiculos.store': (new VehiculoController())->store($_POST); break;
        case 'vehiculos.show': View::render('vehiculos/show', (new VehiculoController())->show($_GET['id'] ?? '')); break;
        case 'vehiculos.edit': View::render('vehiculos/edit', (new VehiculoController())->show($_GET['id'] ?? '')); break;
        case 'vehiculos.update': (new VehiculoController())->update($_POST); break;
        case 'vehiculos.delete': (new VehiculoController())->delete($_POST); break;
    }
} catch (Throwable $e) {
    Flash::set('error', $e->getMessage());
    $fallback = isset($_SESSION['auth']['id']) ? 'home' : 'auth.login';
    header('Location: index.php?route=' . $fallback);
    exit;
}
