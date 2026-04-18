<?php
declare(strict_types=1);
final class AuthController
{
public function authenticate(array $post): void
{
    $command = new LoginCommand($post['email'] ?? '', $post['password'] ?? '');
    $user = DependencyInjection::getLoginUseCase()->execute($command);

    $_SESSION['auth'] = [
        'id' => $user->id()->value(),
        'name' => $user->name()->value(),
        'email' => $user->email()->value(),
        'role' => $user->role(),
    ];

    Flash::set('success', 'Bienvenido, ' . $user->name()->value() . '.');
    header('Location: index.php?route=home');
    exit;
}
    public function logout(): void { $_SESSION = []; session_destroy(); session_start(); Flash::set('success', 'Sesión cerrada correctamente.'); View::redirect('auth.login'); }
    public function forgot(array $post): void { DependencyInjection::getForgotPasswordUseCase()->execute(new ForgotPasswordCommand($post['email'] ?? '')); Flash::set('success', 'Si el correo existe, se envió una contraseña temporal.'); View::redirect('auth.login'); }
}
