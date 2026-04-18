<?php
declare(strict_types=1);
final class VehiculoController
{
    public function index(): array { return ['vehiculos' => DependencyInjection::getGetAllVehiculosUseCase()->execute(new GetAllVehiculosQuery())]; }
    public function store(array $post): void { $post['id'] = bin2hex(random_bytes(16)); DependencyInjection::getCreateVehiculoUseCase()->execute(new CreateVehiculoCommand($post)); Flash::set('success', 'Vehículo creado correctamente.'); View::redirect('vehiculos.index'); }
    public function show(string $id): array { return ['vehiculo' => DependencyInjection::getGetVehiculoByIdUseCase()->execute(new GetVehiculoByIdQuery($id))]; }
    public function update(array $post): void { DependencyInjection::getUpdateVehiculoUseCase()->execute(new UpdateVehiculoCommand($post)); Flash::set('success', 'Vehículo actualizado correctamente.'); View::redirect('vehiculos.index'); }
    public function delete(array $post): void { DependencyInjection::getDeleteVehiculoUseCase()->execute(new DeleteVehiculoCommand($post['id'] ?? '')); Flash::set('success', 'Vehículo eliminado correctamente.'); View::redirect('vehiculos.index'); }
}
