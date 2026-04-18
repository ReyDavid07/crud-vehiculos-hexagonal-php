<?php
declare(strict_types=1);
interface UpdateUserPort { public function update(UserModel $user): UserModel; }
