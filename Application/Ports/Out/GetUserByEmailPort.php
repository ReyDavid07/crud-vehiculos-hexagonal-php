<?php
declare(strict_types=1);
interface GetUserByEmailPort { public function getByEmail(UserEmail $email): ?UserModel; }
