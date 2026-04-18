<?php
declare(strict_types=1);
interface ResetUserPasswordPort { public function updatePassword(UserId $userId, UserPassword $password): void; }
