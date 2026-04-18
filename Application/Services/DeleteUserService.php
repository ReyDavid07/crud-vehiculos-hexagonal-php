<?php
declare(strict_types=1);
final class DeleteUserService implements DeleteUserUseCase
{
    private DeleteUserPort $deleteUserPort; private GetUserByIdPort $getUserByIdPort; public function __construct(DeleteUserPort $deleteUserPort, GetUserByIdPort $getUserByIdPort){$this->deleteUserPort=$deleteUserPort;$this->getUserByIdPort=$getUserByIdPort;}
    public function execute(DeleteUserCommand $command): void { $id = UserApplicationMapper::fromDeleteCommandToUserId($command); if ($this->getUserByIdPort->getById($id) === null) { throw UserNotFoundException::becauseIdWasNotFound($id->value()); } $this->deleteUserPort->delete($id); }
}
