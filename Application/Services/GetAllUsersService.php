<?php
declare(strict_types=1);
final class GetAllUsersService implements GetAllUsersUseCase { private GetAllUsersPort $port; public function __construct(GetAllUsersPort $port){$this->port=$port;} public function execute(GetAllUsersQuery $query): array { return $this->port->getAll(); } }
