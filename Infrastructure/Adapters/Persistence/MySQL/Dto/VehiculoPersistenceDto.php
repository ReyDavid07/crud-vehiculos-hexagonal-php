<?php
declare(strict_types=1);
final class VehiculoPersistenceDto { private array $data; public function __construct(array $data){$this->data=$data;} public function all(): array { return $this->data; } }
