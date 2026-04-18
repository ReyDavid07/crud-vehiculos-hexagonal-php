<?php
declare(strict_types=1);
interface LoginUseCase { public function execute(LoginCommand $command): UserModel; }
