<?php
declare(strict_types=1);
interface GetUserByIdPort { public function getById(UserId $userId): ?UserModel; }
