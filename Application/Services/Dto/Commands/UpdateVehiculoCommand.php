<?php
declare(strict_types=1);
final class UpdateVehiculoCommand { private array $data; public function __construct(array $data){$this->data=array_map(static fn($v)=>is_string($v)?trim($v):$v,$data);} public function get(string $key){ return $this->data[$key] ?? null; } }
