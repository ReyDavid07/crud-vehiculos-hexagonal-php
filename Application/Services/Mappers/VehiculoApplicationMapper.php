<?php
declare(strict_types=1);
final class VehiculoApplicationMapper
{
    public static function fromCreateCommandToModel(CreateVehiculoCommand $command): VehiculoModel { return self::fromArrayToModel($command->get('id'), $command); }
    public static function fromUpdateCommandToModel(UpdateVehiculoCommand $command): VehiculoModel { return self::fromArrayToModel($command->get('id'), $command); }
    private static function fromArrayToModel(string $id, $command): VehiculoModel {
        return new VehiculoModel(
            new VehiculoId($id),
            new VehiculoPlaca($command->get('placa')),
            new VehiculoTexto($command->get('marca'), 'marca'),
            new VehiculoTexto($command->get('modelo'), 'modelo'),
            new VehiculoTexto($command->get('version'), 'version'),
            new VehiculoTexto($command->get('color'), 'color'),
            new VehiculoNumero($command->get('numPuestos'), 'numPuestos'),
            new VehiculoNumero($command->get('numPuertas'), 'numPuertas'),
            new VehiculoTexto($command->get('combustible'), 'combustible'),
            new VehiculoNumero($command->get('kilometros'), 'kilometros'),
            new VehiculoNumero($command->get('cilindraje'), 'cilindraje'),
            new VehiculoTexto($command->get('categoria'), 'categoria')
        );
    }
    public static function fromDeleteCommandToVehiculoId(DeleteVehiculoCommand $command): VehiculoId { return new VehiculoId($command->getId()); }
    public static function fromGetVehiculoByIdQueryToVehiculoId(GetVehiculoByIdQuery $query): VehiculoId { return new VehiculoId($query->getId()); }
}
