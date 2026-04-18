<?php
class InvalidUserIdException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('El ID del usuario no puede estar vacío.'); } }