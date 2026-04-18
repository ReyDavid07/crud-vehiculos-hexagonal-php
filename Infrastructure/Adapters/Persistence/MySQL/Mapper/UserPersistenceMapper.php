<?php
declare(strict_types=1);
final class UserPersistenceMapper
{
    public function fromModelToDto(UserModel $user): UserPersistenceDto { return new UserPersistenceDto($user->id()->value(),$user->name()->value(),$user->email()->value(),$user->password()->value(),$user->role(),$user->status()); }
    public function fromRowToModel(array $row): UserModel { return new UserModel(new UserId((string) $row['id']), new UserName((string) $row['name']), new UserEmail((string) $row['email']), UserPassword::fromHash((string) $row['password']), (string) $row['role'], (string) $row['status']); }
    public function fromRowsToModels(array $rows): array { return array_map(fn($row) => $this->fromRowToModel($row), $rows); }
}
