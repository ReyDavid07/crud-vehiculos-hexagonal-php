<?php
class UserAlreadyExistsException extends DomainException { public static function becauseEmailAlreadyExists($email){ return new self('Ya existe un usuario con el email: ' . $email); } }