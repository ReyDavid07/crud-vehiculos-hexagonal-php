<?php
declare(strict_types=1);
final class VehiculoPersistenceMapper
{
    public function fromModelToDto(VehiculoModel $v): VehiculoPersistenceDto { return new VehiculoPersistenceDto(['id'=>$v->id()->value(),'placa'=>$v->placa()->value(),'marca'=>$v->marca()->value(),'modelo'=>$v->modelo()->value(),'version'=>$v->version()->value(),'color'=>$v->color()->value(),'numPuestos'=>$v->numPuestos()->value(),'numPuertas'=>$v->numPuertas()->value(),'combustible'=>$v->combustible()->value(),'kilometros'=>$v->kilometros()->value(),'cilindraje'=>$v->cilindraje()->value(),'categoria'=>$v->categoria()->value()]); }
    public function fromRowToModel(array $row): VehiculoModel { return new VehiculoModel(new VehiculoId((string)$row['id']),new VehiculoPlaca((string)$row['placa']),new VehiculoTexto((string)$row['marca'],'marca'),new VehiculoTexto((string)$row['modelo'],'modelo'),new VehiculoTexto((string)$row['version'],'version'),new VehiculoTexto((string)$row['color'],'color'),new VehiculoNumero((int)$row['num_puestos'],'numPuestos'),new VehiculoNumero((int)$row['num_puertas'],'numPuertas'),new VehiculoTexto((string)$row['combustible'],'combustible'),new VehiculoNumero((int)$row['kilometros'],'kilometros'),new VehiculoNumero((int)$row['cilindraje'],'cilindraje'),new VehiculoTexto((string)$row['categoria'],'categoria')); }
    public function fromRowsToModels(array $rows): array { return array_map(fn($row)=>$this->fromRowToModel($row), $rows); }
}
