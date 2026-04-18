<?php
declare(strict_types=1);
final class CreateUserService implements CreateUserUseCase
{
    private SaveUserPort $saveUserPort; private GetUserByEmailPort $getUserByEmailPort;
    public function __construct(SaveUserPort $saveUserPort, GetUserByEmailPort $getUserByEmailPort){$this->saveUserPort=$saveUserPort;$this->getUserByEmailPort=$getUserByEmailPort;}
    public function execute(CreateUserCommand $command): UserModel { $email = new UserEmail($command->getEmail()); if ($this->getUserByEmailPort->getByEmail($email) !== null) { throw UserAlreadyExistsException::becauseEmailAlreadyExists($email->value()); } return $this->saveUserPort->save(UserApplicationMapper::fromCreateCommandToModel($command)); }
}
