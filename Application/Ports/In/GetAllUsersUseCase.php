<?php
declare(strict_types=1);
interface GetAllUsersUseCase { public function execute(GetAllUsersQuery $query): array; }
