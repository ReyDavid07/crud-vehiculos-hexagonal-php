<?php
declare(strict_types=1);
interface DeleteUserUseCase { public function execute(DeleteUserCommand $command): void; }
