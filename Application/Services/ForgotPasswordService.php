<?php
declare(strict_types=1);
final class ForgotPasswordService implements ForgotPasswordUseCase
{
    private GetUserByEmailPort $getUserByEmailPort; private ResetUserPasswordPort $resetUserPasswordPort;
    public function __construct(GetUserByEmailPort $getUserByEmailPort, ResetUserPasswordPort $resetUserPasswordPort){$this->getUserByEmailPort=$getUserByEmailPort;$this->resetUserPasswordPort=$resetUserPasswordPort;}
    public function execute(ForgotPasswordCommand $command): void
    {
        try { $email = new UserEmail($command->getEmail()); } catch (Throwable $e) { return; }
        $user = $this->getUserByEmailPort->getByEmail($email);
        if ($user === null) { return; }
        $temp = bin2hex(random_bytes(5));
        $this->resetUserPasswordPort->updatePassword($user->id(), UserPassword::fromPlainText($temp));
        $projectRoot = dirname(__DIR__, 2);
        $html = self::renderEmailTemplate($projectRoot . '/Presentation/Views/emails/forgot-password.php', [
            'name' => $user->name()->value(),
            'email' => $user->email()->value(),
            'temporaryPassword' => $temp,
        ]);
        @mail($user->email()->value(), 'Recuperación de contraseña', $html, "MIME-Version: 1.0
Content-type:text/html;charset=UTF-8
");
    }
    private static function renderEmailTemplate(string $path, array $data): string { extract($data); ob_start(); require $path; return (string) ob_get_clean(); }
}
