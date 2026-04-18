<?php
declare(strict_types=1);
final class VehiculoModel
{
    private VehiculoId $id; private VehiculoPlaca $placa; private VehiculoTexto $marca; private VehiculoTexto $modelo; private VehiculoTexto $version; private VehiculoTexto $color; private VehiculoNumero $numPuestos; private VehiculoNumero $numPuertas; private VehiculoTexto $combustible; private VehiculoNumero $kilometros; private VehiculoNumero $cilindraje; private VehiculoTexto $categoria;
    public function __construct(VehiculoId $id, VehiculoPlaca $placa, VehiculoTexto $marca, VehiculoTexto $modelo, VehiculoTexto $version, VehiculoTexto $color, VehiculoNumero $numPuestos, VehiculoNumero $numPuertas, VehiculoTexto $combustible, VehiculoNumero $kilometros, VehiculoNumero $cilindraje, VehiculoTexto $categoria) {
        $this->id=$id; $this->placa=$placa; $this->marca=$marca; $this->modelo=$modelo; $this->version=$version; $this->color=$color; $this->numPuestos=$numPuestos; $this->numPuertas=$numPuertas; $this->combustible=$combustible; $this->kilometros=$kilometros; $this->cilindraje=$cilindraje; $this->categoria=$categoria;
    }
    public function id(): VehiculoId { return $this->id; } public function placa(): VehiculoPlaca { return $this->placa; } public function marca(): VehiculoTexto { return $this->marca; } public function modelo(): VehiculoTexto { return $this->modelo; } public function version(): VehiculoTexto { return $this->version; } public function color(): VehiculoTexto { return $this->color; } public function numPuestos(): VehiculoNumero { return $this->numPuestos; } public function numPuertas(): VehiculoNumero { return $this->numPuertas; } public function combustible(): VehiculoTexto { return $this->combustible; } public function kilometros(): VehiculoNumero { return $this->kilometros; } public function cilindraje(): VehiculoNumero { return $this->cilindraje; } public function categoria(): VehiculoTexto { return $this->categoria; }
}
