<?php
declare(strict_types=1);
interface ForgotPasswordUseCase { public function execute(ForgotPasswordCommand $command): void; }
