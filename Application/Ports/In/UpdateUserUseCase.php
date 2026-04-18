<?php
declare(strict_types=1);
interface UpdateUserUseCase { public function execute(UpdateUserCommand $command): UserModel; }
