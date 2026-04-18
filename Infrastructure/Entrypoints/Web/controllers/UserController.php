<?php
declare(strict_types=1);
final class UserController
{
    public function index(): array { return ['users' => DependencyInjection::getGetAllUsersUseCase()->execute(new GetAllUsersQuery())]; }
    public function store(array $post): void { $command = new CreateUserCommand(bin2hex(random_bytes(16)), $post['name'] ?? '', $post['email'] ?? '', $post['password'] ?? '', $post['role'] ?? 'MEMBER'); DependencyInjection::getCreateUserUseCase()->execute($command); Flash::set('success', 'Usuario creado correctamente.'); View::redirect('users.index'); }
    public function show(string $id): array { return ['user' => DependencyInjection::getGetUserByIdUseCase()->execute(new GetUserByIdQuery($id))]; }
    public function update(array $post): void { $command = new UpdateUserCommand($post['id'] ?? '', $post['name'] ?? '', $post['email'] ?? '', $post['password'] ?? '', $post['role'] ?? 'MEMBER', $post['status'] ?? 'ACTIVE'); DependencyInjection::getUpdateUserUseCase()->execute($command); Flash::set('success', 'Usuario actualizado correctamente.'); View::redirect('users.index'); }
    public function delete(array $post): void { DependencyInjection::getDeleteUserUseCase()->execute(new DeleteUserCommand($post['id'] ?? '')); Flash::set('success', 'Usuario eliminado correctamente.'); View::redirect('users.index'); }
}
