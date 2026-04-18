<?php
declare(strict_types=1);
final class UpdateUserService implements UpdateUserUseCase
{
    private UpdateUserPort $updateUserPort; private GetUserByIdPort $getUserByIdPort; private GetUserByEmailPort $getUserByEmailPort;
    public function __construct(UpdateUserPort $updateUserPort, GetUserByIdPort $getUserByIdPort, GetUserByEmailPort $getUserByEmailPort){$this->updateUserPort=$updateUserPort;$this->getUserByIdPort=$getUserByIdPort;$this->getUserByEmailPort=$getUserByEmailPort;}
    public function execute(UpdateUserCommand $command): UserModel { $userId = new UserId($command->getId()); $current = $this->getUserByIdPort->getById($userId); if ($current === null) { throw UserNotFoundException::becauseIdWasNotFound($userId->value()); } $email = new UserEmail($command->getEmail()); $same = $this->getUserByEmailPort->getByEmail($email); if ($same !== null && !$same->id()->equals($userId)) { throw UserAlreadyExistsException::becauseEmailAlreadyExists($email->value()); } $password = trim($command->getPassword()) !== '' ? UserPassword::fromPlainText($command->getPassword()) : $current->password(); return $this->updateUserPort->update(new UserModel($userId, new UserName($command->getName()), $email, $password, $command->getRole(), $command->getStatus())); }
}
