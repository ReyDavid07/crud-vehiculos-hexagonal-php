<?php
declare(strict_types=1);
final class GetUserByIdService implements GetUserByIdUseCase { private GetUserByIdPort $port; public function __construct(GetUserByIdPort $port){$this->port=$port;} public function execute(GetUserByIdQuery $query): UserModel { $id = UserApplicationMapper::fromGetUserByIdQueryToUserId($query); $user = $this->port->getById($id); if ($user === null) { throw UserNotFoundException::becauseIdWasNotFound($id->value()); } return $user; } }
