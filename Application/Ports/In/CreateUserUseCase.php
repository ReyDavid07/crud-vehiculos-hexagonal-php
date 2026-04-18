<?php
declare(strict_types=1);
interface CreateUserUseCase { public function execute(CreateUserCommand $command): UserModel; }
