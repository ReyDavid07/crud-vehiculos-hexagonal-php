<?php
declare(strict_types=1);
final class UserApplicationMapper
{
    public static function fromCreateCommandToModel(CreateUserCommand $command): UserModel { return new UserModel(new UserId($command->getId()), new UserName($command->getName()), new UserEmail($command->getEmail()), UserPassword::fromPlainText($command->getPassword()), $command->getRole(), UserStatusEnum::PENDING); }
    public static function fromDeleteCommandToUserId(DeleteUserCommand $command): UserId { return new UserId($command->getId()); }
    public static function fromGetUserByIdQueryToUserId(GetUserByIdQuery $query): UserId { return new UserId($query->getId()); }
}
