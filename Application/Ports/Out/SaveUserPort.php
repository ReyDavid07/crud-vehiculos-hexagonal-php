<?php
declare(strict_types=1);
interface SaveUserPort { public function save(UserModel $user): UserModel; }
