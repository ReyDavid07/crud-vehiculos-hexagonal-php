<?php
declare(strict_types=1);
interface DeleteUserPort { public function delete(UserId $userId): void; }
