<?php
declare(strict_types=1);
final class ForgotPasswordCommand { private string $email; public function __construct(string $email){$this->email=trim($email);} public function getEmail(): string { return $this->email; }}
