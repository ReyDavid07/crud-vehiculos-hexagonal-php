<?php
declare(strict_types=1);
interface GetUserByIdUseCase { public function execute(GetUserByIdQuery $query): UserModel; }
