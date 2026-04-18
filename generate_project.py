from pathlib import Path

base = Path('/mnt/data/vehiculo_hexagonal_project')
files = {}

def add(path, content):
    files[path] = content.lstrip('\n')

# Common
add('Common/ClassLoader.php', '''
<?php
declare(strict_types=1);

final class ClassLoader
{
    public static function register(string $projectRoot): void
    {
        spl_autoload_register(function (string $className) use ($projectRoot): void {
            $iterator = new RecursiveIteratorIterator(
                new RecursiveDirectoryIterator($projectRoot, FilesystemIterator::SKIP_DOTS)
            );

            foreach ($iterator as $file) {
                if (!$file->isFile() || $file->getExtension() !== 'php') {
                    continue;
                }

                if ($file->getBasename('.php') === $className) {
                    require_once $file->getPathname();
                    return;
                }
            }
        });
    }
}
''')

add('Common/DependencyInjection.php', '''
<?php
declare(strict_types=1);

require_once __DIR__ . '/ClassLoader.php';

final class DependencyInjection
{
    private static ?PDO $pdo = null;
    private static ?UserRepositoryMySQL $userRepository = null;
    private static ?VehiculoRepositoryMySQL $vehiculoRepository = null;

    public static function bootstrap(string $projectRoot): void
    {
        ClassLoader::register($projectRoot);
    }

    public static function getPdo(): PDO
    {
        if (self::$pdo === null) {
            $config = require __DIR__ . '/../config/database.php';
            $connection = new Connection(
                $config['host'],
                (int) $config['port'],
                $config['database'],
                $config['username'],
                $config['password'],
                $config['charset']
            );
            self::$pdo = $connection->createPdo();
        }

        return self::$pdo;
    }

    public static function getUserRepository(): UserRepositoryMySQL
    {
        if (self::$userRepository === null) {
            self::$userRepository = new UserRepositoryMySQL(self::getPdo(), new UserPersistenceMapper());
        }
        return self::$userRepository;
    }

    public static function getVehiculoRepository(): VehiculoRepositoryMySQL
    {
        if (self::$vehiculoRepository === null) {
            self::$vehiculoRepository = new VehiculoRepositoryMySQL(self::getPdo(), new VehiculoPersistenceMapper());
        }
        return self::$vehiculoRepository;
    }

    public static function getCreateUserUseCase(): CreateUserUseCase
    {
        $repository = self::getUserRepository();
        return new CreateUserService($repository, $repository);
    }

    public static function getUpdateUserUseCase(): UpdateUserUseCase
    {
        $repository = self::getUserRepository();
        return new UpdateUserService($repository, $repository, $repository);
    }

    public static function getDeleteUserUseCase(): DeleteUserUseCase
    {
        $repository = self::getUserRepository();
        return new DeleteUserService($repository, $repository);
    }

    public static function getGetUserByIdUseCase(): GetUserByIdUseCase
    {
        return new GetUserByIdService(self::getUserRepository());
    }

    public static function getGetAllUsersUseCase(): GetAllUsersUseCase
    {
        return new GetAllUsersService(self::getUserRepository());
    }

    public static function getLoginUseCase(): LoginUseCase
    {
        return new LoginService(self::getUserRepository());
    }

    public static function getForgotPasswordUseCase(): ForgotPasswordUseCase
    {
        return new ForgotPasswordService(self::getUserRepository(), self::getUserRepository());
    }

    public static function getCreateVehiculoUseCase(): CreateVehiculoUseCase
    {
        $repository = self::getVehiculoRepository();
        return new CreateVehiculoService($repository, $repository);
    }

    public static function getUpdateVehiculoUseCase(): UpdateVehiculoUseCase
    {
        $repository = self::getVehiculoRepository();
        return new UpdateVehiculoService($repository, $repository, $repository);
    }

    public static function getDeleteVehiculoUseCase(): DeleteVehiculoUseCase
    {
        $repository = self::getVehiculoRepository();
        return new DeleteVehiculoService($repository, $repository);
    }

    public static function getGetVehiculoByIdUseCase(): GetVehiculoByIdUseCase
    {
        return new GetVehiculoByIdService(self::getVehiculoRepository());
    }

    public static function getGetAllVehiculosUseCase(): GetAllVehiculosUseCase
    {
        return new GetAllVehiculosService(self::getVehiculoRepository());
    }
}
''')

add('config/database.php', '''
<?php
return [
    'host' => '127.0.0.1',
    'port' => 3306,
    'database' => 'crud_vehiculos',
    'username' => 'root',
    'password' => '',
    'charset' => 'utf8mb4',
];
''')

# Domain exceptions/enums/value objects/models minimal reusable helpers for User
user_exceptions = {
'InvalidUserIdException.php': '''<?php\nclass InvalidUserIdException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('El ID del usuario no puede estar vacío.'); } }''',
'InvalidUserNameException.php': '''<?php\nclass InvalidUserNameException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('El nombre del usuario no puede estar vacío.'); } public static function becauseLengthIsTooShort($min){ return new self('El nombre del usuario debe tener al menos ' . $min . ' caracteres.'); } }''',
'InvalidUserEmailException.php': '''<?php\nclass InvalidUserEmailException extends InvalidArgumentException { public static function becauseFormatIsInvalid($email){ return new self('El formato del email es inválido: ' . $email); } public static function becauseValueIsEmpty(){ return new self('El email del usuario no puede estar vacío.'); } }''',
'InvalidUserPasswordException.php': '''<?php\nclass InvalidUserPasswordException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self('La contraseña no puede estar vacía.'); } public static function becauseLengthIsTooShort($min){ return new self('La contraseña debe tener al menos ' . $min . ' caracteres.'); } }''',
'InvalidUserRoleException.php': '''<?php\nclass InvalidUserRoleException extends InvalidArgumentException { public static function becauseValueIsInvalid($value){ return new self('El rol "' . $value . '" no es válido.'); } }''',
'InvalidUserStatusException.php': '''<?php\nclass InvalidUserStatusException extends InvalidArgumentException { public static function becauseValueIsInvalid($value){ return new self('El estado "' . $value . '" no es válido.'); } }''',
'UserAlreadyExistsException.php': '''<?php\nclass UserAlreadyExistsException extends DomainException { public static function becauseEmailAlreadyExists($email){ return new self('Ya existe un usuario con el email: ' . $email); } }''',
'UserNotFoundException.php': '''<?php\nclass UserNotFoundException extends DomainException { public static function becauseIdWasNotFound($id){ return new self('No se encontró un usuario con el ID: ' . $id); } }''',
'InvalidCredentialsException.php': '''<?php\ndeclare(strict_types=1);\nfinal class InvalidCredentialsException extends RuntimeException { public static function becauseCredentialsAreInvalid(): self { return new self('Correo o contraseña incorrectos.'); } public static function becauseUserIsNotActive(): self { return new self('Tu cuenta no está activa. Contacta al administrador.'); } }''',
}
for name, content in user_exceptions.items(): add(f'Domain/Exceptions/{name}', content)

add('Domain/Enums/UserRoleEnum.php', '''
<?php
class UserRoleEnum
{
    public const ADMIN = 'ADMIN';
    public const MEMBER = 'MEMBER';
    public const REVIEWER = 'REVIEWER';
    public static function values(): array { return [self::ADMIN, self::MEMBER, self::REVIEWER]; }
    public static function isValid(string $value): bool { return in_array($value, self::values(), true); }
    public static function ensureIsValid(string $value): void { if (!self::isValid($value)) { throw InvalidUserRoleException::becauseValueIsInvalid($value); } }
}
''')
add('Domain/Enums/UserStatusEnum.php', '''
<?php
class UserStatusEnum
{
    public const ACTIVE = 'ACTIVE';
    public const INACTIVE = 'INACTIVE';
    public const PENDING = 'PENDING';
    public const BLOCKED = 'BLOCKED';
    public static function values(): array { return [self::ACTIVE, self::INACTIVE, self::PENDING, self::BLOCKED]; }
    public static function isValid(string $value): bool { return in_array($value, self::values(), true); }
    public static function ensureIsValid(string $value): void { if (!self::isValid($value)) { throw InvalidUserStatusException::becauseValueIsInvalid($value); } }
}
''')
add('Domain/ValueObjects/UserId.php', '''
<?php
class UserId
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserIdException::becauseValueIsEmpty(); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(UserId $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
''')
add('Domain/ValueObjects/UserName.php', '''
<?php
class UserName
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserNameException::becauseValueIsEmpty(); } if (mb_strlen($normalized) < 3) { throw InvalidUserNameException::becauseLengthIsTooShort(3); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(UserName $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
''')
add('Domain/ValueObjects/UserEmail.php', '''
<?php
class UserEmail
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserEmailException::becauseValueIsEmpty(); } if (!filter_var($normalized, FILTER_VALIDATE_EMAIL)) { throw InvalidUserEmailException::becauseFormatIsInvalid($normalized); } $this->value = strtolower($normalized); }
    public function value(): string { return $this->value; }
    public function equals(UserEmail $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
''')
add('Domain/ValueObjects/UserPassword.php', '''
<?php
class UserPassword
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidUserPasswordException::becauseValueIsEmpty(); } if (strlen($normalized) < 8) { throw InvalidUserPasswordException::becauseLengthIsTooShort(8); } $this->value = $normalized; }
    public static function fromPlainText(string $raw): self { $normalized = trim($raw); if ($normalized === '') { throw InvalidUserPasswordException::becauseValueIsEmpty(); } if (strlen($normalized) < 8) { throw InvalidUserPasswordException::becauseLengthIsTooShort(8); } return new self(password_hash($normalized, PASSWORD_BCRYPT)); }
    public static function fromHash(string $hash): self { return new self($hash); }
    public function verifyPlain(string $plain): bool { return password_verify($plain, $this->value); }
    public function value(): string { return $this->value; }
    public function equals(UserPassword $other): bool { return $this->value === $other->value(); }
    public function __toString(): string { return $this->value; }
}
''')
add('Domain/Models/UserModel.php', '''
<?php
declare(strict_types=1);
final class UserModel
{
    private UserId $id; private UserName $name; private UserEmail $email; private UserPassword $password; private string $role; private string $status;
    public function __construct(UserId $id, UserName $name, UserEmail $email, UserPassword $password, string $role, string $status) {
        UserRoleEnum::ensureIsValid($role); UserStatusEnum::ensureIsValid($status);
        $this->id = $id; $this->name = $name; $this->email = $email; $this->password = $password; $this->role = $role; $this->status = $status;
    }
    public static function create(UserId $id, UserName $name, UserEmail $email, UserPassword $password, string $role): self { return new self($id, $name, $email, $password, $role, UserStatusEnum::PENDING); }
    public function id(): UserId { return $this->id; } public function name(): UserName { return $this->name; } public function email(): UserEmail { return $this->email; }
    public function password(): UserPassword { return $this->password; } public function role(): string { return $this->role; } public function status(): string { return $this->status; }
}
''')

# Vehicle domain
veh_exc = {
'InvalidVehiculoIdException.php': 'class InvalidVehiculoIdException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self(\'El ID del vehículo no puede estar vacío.\'); } }',
'InvalidVehiculoPlacaException.php': 'class InvalidVehiculoPlacaException extends InvalidArgumentException { public static function becauseValueIsEmpty(){ return new self(\'La placa no puede estar vacía.\'); } public static function becauseFormatIsInvalid($value){ return new self(\'La placa no es válida: \'. $value); } }',
'InvalidVehiculoTextoException.php': 'class InvalidVehiculoTextoException extends InvalidArgumentException { public static function becauseValueIsEmpty($field){ return new self(\'El campo \'. $field .\' no puede estar vacío.\'); } }',
'InvalidVehiculoNumeroException.php': 'class InvalidVehiculoNumeroException extends InvalidArgumentException { public static function becauseValueIsInvalid($field){ return new self(\'El campo \'. $field .\' debe ser un número válido mayor o igual a cero.\'); } }',
'VehiculoAlreadyExistsException.php': 'class VehiculoAlreadyExistsException extends DomainException { public static function becausePlacaAlreadyExists($placa){ return new self(\'Ya existe un vehículo con la placa: \'. $placa); } }',
'VehiculoNotFoundException.php': 'class VehiculoNotFoundException extends DomainException { public static function becauseIdWasNotFound($id){ return new self(\'No se encontró un vehículo con el ID: \'. $id); } }',
}
for name, body in veh_exc.items(): add(f'Domain/Exceptions/{name}', f'<?php\n{body}\n')

add('Domain/ValueObjects/VehiculoId.php', '''
<?php
class VehiculoId
{
    private string $value;
    public function __construct($value) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidVehiculoIdException::becauseValueIsEmpty(); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(VehiculoId $other): bool { return $this->value === $other->value(); }
}
''')
add('Domain/ValueObjects/VehiculoPlaca.php', '''
<?php
class VehiculoPlaca
{
    private string $value;
    public function __construct($value) { $normalized = strtoupper(trim((string) $value)); if ($normalized === '') { throw InvalidVehiculoPlacaException::becauseValueIsEmpty(); } if (!preg_match('/^[A-Z0-9-]{5,10}$/', $normalized)) { throw InvalidVehiculoPlacaException::becauseFormatIsInvalid($normalized); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
    public function equals(VehiculoPlaca $other): bool { return $this->value === $other->value(); }
}
''')
add('Domain/ValueObjects/VehiculoTexto.php', '''
<?php
class VehiculoTexto
{
    private string $value;
    public function __construct($value, string $field) { $normalized = trim((string) $value); if ($normalized === '') { throw InvalidVehiculoTextoException::becauseValueIsEmpty($field); } $this->value = $normalized; }
    public function value(): string { return $this->value; }
}
''')
add('Domain/ValueObjects/VehiculoNumero.php', '''
<?php
class VehiculoNumero
{
    private int $value;
    public function __construct($value, string $field) { if (!is_numeric($value) || (int) $value < 0) { throw InvalidVehiculoNumeroException::becauseValueIsInvalid($field); } $this->value = (int) $value; }
    public function value(): int { return $this->value; }
}
''')
add('Domain/Models/VehiculoModel.php', '''
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
''')

# Application DTOs
add('Application/Services/Dto/Commands/CreateUserCommand.php', '''
<?php
declare(strict_types=1);
final class CreateUserCommand { private string $id; private string $name; private string $email; private string $password; private string $role; public function __construct(string $id,string $name,string $email,string $password,string $role){$this->id=trim($id);$this->name=trim($name);$this->email=trim($email);$this->password=trim($password);$this->role=trim($role);} public function getId(): string { return $this->id; } public function getName(): string { return $this->name; } public function getEmail(): string { return $this->email; } public function getPassword(): string { return $this->password; } public function getRole(): string { return $this->role; }}
''')
add('Application/Services/Dto/Commands/UpdateUserCommand.php', '''
<?php
declare(strict_types=1);
final class UpdateUserCommand { private string $id; private string $name; private string $email; private string $password; private string $role; private string $status; public function __construct(string $id,string $name,string $email,string $password,string $role,string $status){$this->id=trim($id);$this->name=trim($name);$this->email=trim($email);$this->password=$password;$this->role=trim($role);$this->status=trim($status);} public function getId(): string { return $this->id; } public function getName(): string { return $this->name; } public function getEmail(): string { return $this->email; } public function getPassword(): string { return $this->password; } public function getRole(): string { return $this->role; } public function getStatus(): string { return $this->status; }}
''')
add('Application/Services/Dto/Commands/DeleteUserCommand.php', '''
<?php
declare(strict_types=1);
final class DeleteUserCommand { private string $id; public function __construct(string $id){$this->id=trim($id);} public function getId(): string { return $this->id; }}
''')
add('Application/Services/Dto/Commands/LoginCommand.php', '''
<?php
declare(strict_types=1);
final class LoginCommand { private string $email; private string $password; public function __construct(string $email,string $password){$this->email=trim($email);$this->password=$password;} public function getEmail(): string { return $this->email; } public function getPassword(): string { return $this->password; }}
''')
add('Application/Services/Dto/Commands/ForgotPasswordCommand.php', '''
<?php
declare(strict_types=1);
final class ForgotPasswordCommand { private string $email; public function __construct(string $email){$this->email=trim($email);} public function getEmail(): string { return $this->email; }}
''')
add('Application/Services/Dto/Queries/GetUserByIdQuery.php', '''
<?php
declare(strict_types=1);
final class GetUserByIdQuery { private string $id; public function __construct(string $id){$this->id=trim($id);} public function getId(): string { return $this->id; }}
''')
add('Application/Services/Dto/Queries/GetAllUsersQuery.php', '''
<?php
declare(strict_types=1);
final class GetAllUsersQuery {}
''')

# Vehicle DTOs
for name, fields in {
'CreateVehiculoCommand.php': 'id,placa,marca,modelo,version,color,numPuestos,numPuertas,combustible,kilometros,cilindraje,categoria',
'UpdateVehiculoCommand.php': 'id,placa,marca,modelo,version,color,numPuestos,numPuertas,combustible,kilometros,cilindraje,categoria',
'GetVehiculoByIdQuery.php': 'id',
'GetAllVehiculosQuery.php': '',
'Get': ''}.items():
    pass
add('Application/Services/Dto/Commands/CreateVehiculoCommand.php', '''
<?php
declare(strict_types=1);
final class CreateVehiculoCommand { private array $data; public function __construct(array $data){$this->data=array_map(static fn($v)=>is_string($v)?trim($v):$v,$data);} public function get(string $key){ return $this->data[$key] ?? null; } }
''')
add('Application/Services/Dto/Commands/UpdateVehiculoCommand.php', '''
<?php
declare(strict_types=1);
final class UpdateVehiculoCommand { private array $data; public function __construct(array $data){$this->data=array_map(static fn($v)=>is_string($v)?trim($v):$v,$data);} public function get(string $key){ return $this->data[$key] ?? null; } }
''')
add('Application/Services/Dto/Commands/DeleteVehiculoCommand.php', '''
<?php
declare(strict_types=1);
final class DeleteVehiculoCommand { private string $id; public function __construct(string $id){$this->id=trim($id);} public function getId(): string { return $this->id; } }
''')
add('Application/Services/Dto/Queries/GetVehiculoByIdQuery.php', '''
<?php
declare(strict_types=1);
final class GetVehiculoByIdQuery { private string $id; public function __construct(string $id){$this->id=trim($id);} public function getId(): string { return $this->id; } }
''')
add('Application/Services/Dto/Queries/GetAllVehiculosQuery.php', '''
<?php
declare(strict_types=1);
final class GetAllVehiculosQuery {}
''')

# Ports Users
ports_out = {
'SaveUserPort.php':'public function save(UserModel $user): UserModel;',
'UpdateUserPort.php':'public function update(UserModel $user): UserModel;',
'DeleteUserPort.php':'public function delete(UserId $userId): void;',
'GetUserByIdPort.php':'public function getById(UserId $userId): ?UserModel;',
'GetUserByEmailPort.php':'public function getByEmail(UserEmail $email): ?UserModel;',
'GetAllUsersPort.php':'public function getAll(): array;',
'ResetUserPasswordPort.php':'public function updatePassword(UserId $userId, UserPassword $password): void;',
}
for name, sig in ports_out.items(): add(f'Application/Ports/Out/{name}', f'<?php\ndeclare(strict_types=1);\ninterface {name[:-4]} {{ {sig} }}\n')

ports_in = {
'CreateUserUseCase.php':'public function execute(CreateUserCommand $command): UserModel;',
'UpdateUserUseCase.php':'public function execute(UpdateUserCommand $command): UserModel;',
'DeleteUserUseCase.php':'public function execute(DeleteUserCommand $command): void;',
'GetUserByIdUseCase.php':'public function execute(GetUserByIdQuery $query): UserModel;',
'GetAllUsersUseCase.php':'public function execute(GetAllUsersQuery $query): array;',
'LoginUseCase.php':'public function execute(LoginCommand $command): UserModel;',
'ForgotPasswordUseCase.php':'public function execute(ForgotPasswordCommand $command): void;',
}
for name, sig in ports_in.items(): add(f'Application/Ports/In/{name}', f'<?php\ndeclare(strict_types=1);\ninterface {name[:-4]} {{ {sig} }}\n')

# Vehicle ports
veh_out = {
'SaveVehiculoPort.php':'public function save(VehiculoModel $vehiculo): VehiculoModel;',
'UpdateVehiculoPort.php':'public function update(VehiculoModel $vehiculo): VehiculoModel;',
'DeleteVehiculoPort.php':'public function delete(VehiculoId $vehiculoId): void;',
'GetVehiculoByIdPort.php':'public function getById(VehiculoId $vehiculoId): ?VehiculoModel;',
'GetVehiculoByPlacaPort.php':'public function getByPlaca(VehiculoPlaca $placa): ?VehiculoModel;',
'GetAllVehiculosPort.php':'public function getAll(): array;',
}
for name, sig in veh_out.items(): add(f'Application/Ports/Out/{name}', f'<?php\ndeclare(strict_types=1);\ninterface {name[:-4]} {{ {sig} }}\n')
veh_in = {
'CreateVehiculoUseCase.php':'public function execute(CreateVehiculoCommand $command): VehiculoModel;',
'UpdateVehiculoUseCase.php':'public function execute(UpdateVehiculoCommand $command): VehiculoModel;',
'DeleteVehiculoUseCase.php':'public function execute(DeleteVehiculoCommand $command): void;',
'GetVehiculoByIdUseCase.php':'public function execute(GetVehiculoByIdQuery $query): VehiculoModel;',
'GetAllVehiculosUseCase.php':'public function execute(GetAllVehiculosQuery $query): array;',
}
for name, sig in veh_in.items(): add(f'Application/Ports/In/{name}', f'<?php\ndeclare(strict_types=1);\ninterface {name[:-4]} {{ {sig} }}\n')

# Mappers/services
add('Application/Services/Mappers/UserApplicationMapper.php', '''
<?php
declare(strict_types=1);
final class UserApplicationMapper
{
    public static function fromCreateCommandToModel(CreateUserCommand $command): UserModel { return new UserModel(new UserId($command->getId()), new UserName($command->getName()), new UserEmail($command->getEmail()), UserPassword::fromPlainText($command->getPassword()), $command->getRole(), UserStatusEnum::PENDING); }
    public static function fromDeleteCommandToUserId(DeleteUserCommand $command): UserId { return new UserId($command->getId()); }
    public static function fromGetUserByIdQueryToUserId(GetUserByIdQuery $query): UserId { return new UserId($query->getId()); }
}
''')
add('Application/Services/Mappers/VehiculoApplicationMapper.php', '''
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
''')

# Services users
add('Application/Services/CreateUserService.php', '''
<?php
declare(strict_types=1);
final class CreateUserService implements CreateUserUseCase
{
    private SaveUserPort $saveUserPort; private GetUserByEmailPort $getUserByEmailPort;
    public function __construct(SaveUserPort $saveUserPort, GetUserByEmailPort $getUserByEmailPort){$this->saveUserPort=$saveUserPort;$this->getUserByEmailPort=$getUserByEmailPort;}
    public function execute(CreateUserCommand $command): UserModel { $email = new UserEmail($command->getEmail()); if ($this->getUserByEmailPort->getByEmail($email) !== null) { throw UserAlreadyExistsException::becauseEmailAlreadyExists($email->value()); } return $this->saveUserPort->save(UserApplicationMapper::fromCreateCommandToModel($command)); }
}
''')
add('Application/Services/UpdateUserService.php', '''
<?php
declare(strict_types=1);
final class UpdateUserService implements UpdateUserUseCase
{
    private UpdateUserPort $updateUserPort; private GetUserByIdPort $getUserByIdPort; private GetUserByEmailPort $getUserByEmailPort;
    public function __construct(UpdateUserPort $updateUserPort, GetUserByIdPort $getUserByIdPort, GetUserByEmailPort $getUserByEmailPort){$this->updateUserPort=$updateUserPort;$this->getUserByIdPort=$getUserByIdPort;$this->getUserByEmailPort=$getUserByEmailPort;}
    public function execute(UpdateUserCommand $command): UserModel { $userId = new UserId($command->getId()); $current = $this->getUserByIdPort->getById($userId); if ($current === null) { throw UserNotFoundException::becauseIdWasNotFound($userId->value()); } $email = new UserEmail($command->getEmail()); $same = $this->getUserByEmailPort->getByEmail($email); if ($same !== null && !$same->id()->equals($userId)) { throw UserAlreadyExistsException::becauseEmailAlreadyExists($email->value()); } $password = trim($command->getPassword()) !== '' ? UserPassword::fromPlainText($command->getPassword()) : $current->password(); return $this->updateUserPort->update(new UserModel($userId, new UserName($command->getName()), $email, $password, $command->getRole(), $command->getStatus())); }
}
''')
add('Application/Services/DeleteUserService.php', '''
<?php
declare(strict_types=1);
final class DeleteUserService implements DeleteUserUseCase
{
    private DeleteUserPort $deleteUserPort; private GetUserByIdPort $getUserByIdPort; public function __construct(DeleteUserPort $deleteUserPort, GetUserByIdPort $getUserByIdPort){$this->deleteUserPort=$deleteUserPort;$this->getUserByIdPort=$getUserByIdPort;}
    public function execute(DeleteUserCommand $command): void { $id = UserApplicationMapper::fromDeleteCommandToUserId($command); if ($this->getUserByIdPort->getById($id) === null) { throw UserNotFoundException::becauseIdWasNotFound($id->value()); } $this->deleteUserPort->delete($id); }
}
''')
add('Application/Services/GetUserByIdService.php', '''
<?php
declare(strict_types=1);
final class GetUserByIdService implements GetUserByIdUseCase { private GetUserByIdPort $port; public function __construct(GetUserByIdPort $port){$this->port=$port;} public function execute(GetUserByIdQuery $query): UserModel { $id = UserApplicationMapper::fromGetUserByIdQueryToUserId($query); $user = $this->port->getById($id); if ($user === null) { throw UserNotFoundException::becauseIdWasNotFound($id->value()); } return $user; } }
''')
add('Application/Services/GetAllUsersService.php', '''
<?php
declare(strict_types=1);
final class GetAllUsersService implements GetAllUsersUseCase { private GetAllUsersPort $port; public function __construct(GetAllUsersPort $port){$this->port=$port;} public function execute(GetAllUsersQuery $query): array { return $this->port->getAll(); } }
''')
add('Application/Services/LoginService.php', '''
<?php
declare(strict_types=1);
final class LoginService implements LoginUseCase { private GetUserByEmailPort $port; public function __construct(GetUserByEmailPort $port){$this->port=$port;} public function execute(LoginCommand $command): UserModel { $email = new UserEmail($command->getEmail()); $user = $this->port->getByEmail($email); if ($user === null || !$user->password()->verifyPlain($command->getPassword())) { throw InvalidCredentialsException::becauseCredentialsAreInvalid(); } if ($user->status() !== UserStatusEnum::ACTIVE) { throw InvalidCredentialsException::becauseUserIsNotActive(); } return $user; } }
''')
add('Application/Services/ForgotPasswordService.php', '''
<?php
declare(strict_types=1);
final class ForgotPasswordService implements ForgotPasswordUseCase
{
    private GetUserByEmailPort $getUserByEmailPort; private ResetUserPasswordPort $resetUserPasswordPort;
    public function __construct(GetUserByEmailPort $getUserByEmailPort, ResetUserPasswordPort $resetUserPasswordPort){$this->getUserByEmailPort=$getUserByEmailPort;$this->resetUserPasswordPort=$resetUserPasswordPort;}
    public function execute(ForgotPasswordCommand $command): void
    {
        try { $email = new UserEmail($command->getEmail()); } catch (Throwable $e) { return; }
        $user = $this->getUserByEmailPort->getByEmail($email);
        if ($user === null) { return; }
        $temp = bin2hex(random_bytes(5));
        $this->resetUserPasswordPort->updatePassword($user->id(), UserPassword::fromPlainText($temp));
        $projectRoot = dirname(__DIR__, 2);
        $html = self::renderEmailTemplate($projectRoot . '/Presentation/Views/emails/forgot-password.php', [
            'name' => $user->name()->value(),
            'email' => $user->email()->value(),
            'temporaryPassword' => $temp,
        ]);
        @mail($user->email()->value(), 'Recuperación de contraseña', $html, "MIME-Version: 1.0\r\nContent-type:text/html;charset=UTF-8\r\n");
    }
    private static function renderEmailTemplate(string $path, array $data): string { extract($data); ob_start(); require $path; return (string) ob_get_clean(); }
}
''')

# Vehicle services
for name, content in {
'CreateVehiculoService.php': '''final class CreateVehiculoService implements CreateVehiculoUseCase { private SaveVehiculoPort $savePort; private GetVehiculoByPlacaPort $placaPort; public function __construct(SaveVehiculoPort $savePort, GetVehiculoByPlacaPort $placaPort){$this->savePort=$savePort;$this->placaPort=$placaPort;} public function execute(CreateVehiculoCommand $command): VehiculoModel { $placa = new VehiculoPlaca((string) $command->get('placa')); if ($this->placaPort->getByPlaca($placa)!==null){ throw VehiculoAlreadyExistsException::becausePlacaAlreadyExists($placa->value()); } return $this->savePort->save(VehiculoApplicationMapper::fromCreateCommandToModel($command)); } }''',
'UpdateVehiculoService.php': '''final class UpdateVehiculoService implements UpdateVehiculoUseCase { private UpdateVehiculoPort $updatePort; private GetVehiculoByIdPort $idPort; private GetVehiculoByPlacaPort $placaPort; public function __construct(UpdateVehiculoPort $updatePort, GetVehiculoByIdPort $idPort, GetVehiculoByPlacaPort $placaPort){$this->updatePort=$updatePort;$this->idPort=$idPort;$this->placaPort=$placaPort;} public function execute(UpdateVehiculoCommand $command): VehiculoModel { $id = new VehiculoId((string) $command->get('id')); if ($this->idPort->getById($id)===null){ throw VehiculoNotFoundException::becauseIdWasNotFound($id->value()); } $placa = new VehiculoPlaca((string) $command->get('placa')); $same = $this->placaPort->getByPlaca($placa); if ($same!==null && !$same->id()->equals($id)){ throw VehiculoAlreadyExistsException::becausePlacaAlreadyExists($placa->value()); } return $this->updatePort->update(VehiculoApplicationMapper::fromUpdateCommandToModel($command)); } }''',
'DeleteVehiculoService.php': '''final class DeleteVehiculoService implements DeleteVehiculoUseCase { private DeleteVehiculoPort $deletePort; private GetVehiculoByIdPort $idPort; public function __construct(DeleteVehiculoPort $deletePort, GetVehiculoByIdPort $idPort){$this->deletePort=$deletePort;$this->idPort=$idPort;} public function execute(DeleteVehiculoCommand $command): void { $id = VehiculoApplicationMapper::fromDeleteCommandToVehiculoId($command); if ($this->idPort->getById($id)===null){ throw VehiculoNotFoundException::becauseIdWasNotFound($id->value()); } $this->deletePort->delete($id); } }''',
'GetVehiculoByIdService.php': '''final class GetVehiculoByIdService implements GetVehiculoByIdUseCase { private GetVehiculoByIdPort $port; public function __construct(GetVehiculoByIdPort $port){$this->port=$port;} public function execute(GetVehiculoByIdQuery $query): VehiculoModel { $id = VehiculoApplicationMapper::fromGetVehiculoByIdQueryToVehiculoId($query); $vehiculo = $this->port->getById($id); if ($vehiculo===null){ throw VehiculoNotFoundException::becauseIdWasNotFound($id->value()); } return $vehiculo; } }''',
'GetAllVehiculosService.php': '''final class GetAllVehiculosService implements GetAllVehiculosUseCase { private GetAllVehiculosPort $port; public function __construct(GetAllVehiculosPort $port){$this->port=$port;} public function execute(GetAllVehiculosQuery $query): array { return $this->port->getAll(); } }'''
}.items():
    add(f'Application/Services/{name}', f'<?php\ndeclare(strict_types=1);\n{content}\n')

# Infrastructure users
add('Infrastructure/Adapters/Persistence/MySQL/Config/Connection.php', '''
<?php
declare(strict_types=1);
final class Connection
{
    private string $host; private int $port; private string $database; private string $username; private string $password; private string $charset;
    public function __construct(string $host, int $port, string $database, string $username, string $password, string $charset = 'utf8mb4') {$this->host=$host;$this->port=$port;$this->database=$database;$this->username=$username;$this->password=$password;$this->charset=$charset;}
    public function createPdo(): PDO { $dsn = sprintf('mysql:host=%s;port=%d;dbname=%s;charset=%s',$this->host,$this->port,$this->database,$this->charset); return new PDO($dsn,$this->username,$this->password,[PDO::ATTR_ERRMODE=>PDO::ERRMODE_EXCEPTION,PDO::ATTR_DEFAULT_FETCH_MODE=>PDO::FETCH_ASSOC,PDO::ATTR_EMULATE_PREPARES=>false]); }
}
''')
add('Infrastructure/Adapters/Persistence/MySQL/Dto/UserPersistenceDto.php', '''<?php
declare(strict_types=1);
final class UserPersistenceDto { private string $id; private string $name; private string $email; private string $password; private string $role; private string $status; public function __construct(string $id,string $name,string $email,string $password,string $role,string $status){$this->id=trim($id);$this->name=trim($name);$this->email=trim($email);$this->password=trim($password);$this->role=trim($role);$this->status=trim($status);} public function id(): string { return $this->id; } public function name(): string { return $this->name; } public function email(): string { return $this->email; } public function password(): string { return $this->password; } public function role(): string { return $this->role; } public function status(): string { return $this->status; } }
''')
add('Infrastructure/Adapters/Persistence/MySQL/Entity/UserEntity.php', '''<?php
declare(strict_types=1);
final class UserEntity { private string $id; private string $name; private string $email; private string $password; private string $role; private string $status; private ?string $createdAt; private ?string $updatedAt; public function __construct(string $id,string $name,string $email,string $password,string $role,string $status,?string $createdAt=null,?string $updatedAt=null){$this->id=$id;$this->name=$name;$this->email=$email;$this->password=$password;$this->role=$role;$this->status=$status;$this->createdAt=$createdAt;$this->updatedAt=$updatedAt;} public function id(): string { return $this->id; } public function name(): string { return $this->name; } public function email(): string { return $this->email; } public function password(): string { return $this->password; } public function role(): string { return $this->role; } public function status(): string { return $this->status; } }
''')
add('Infrastructure/Adapters/Persistence/MySQL/Mapper/UserPersistenceMapper.php', '''
<?php
declare(strict_types=1);
final class UserPersistenceMapper
{
    public function fromModelToDto(UserModel $user): UserPersistenceDto { return new UserPersistenceDto($user->id()->value(),$user->name()->value(),$user->email()->value(),$user->password()->value(),$user->role(),$user->status()); }
    public function fromRowToModel(array $row): UserModel { return new UserModel(new UserId((string) $row['id']), new UserName((string) $row['name']), new UserEmail((string) $row['email']), UserPassword::fromHash((string) $row['password']), (string) $row['role'], (string) $row['status']); }
    public function fromRowsToModels(array $rows): array { return array_map(fn($row) => $this->fromRowToModel($row), $rows); }
}
''')
add('Infrastructure/Adapters/Persistence/MySQL/Repository/UserRepositoryMySQL.php', '''
<?php
declare(strict_types=1);
final class UserRepositoryMySQL implements SaveUserPort, UpdateUserPort, GetUserByIdPort, GetUserByEmailPort, GetAllUsersPort, DeleteUserPort, ResetUserPasswordPort
{
    private PDO $pdo; private UserPersistenceMapper $mapper;
    public function __construct(PDO $pdo, UserPersistenceMapper $mapper){$this->pdo=$pdo;$this->mapper=$mapper;}
    public function save(UserModel $user): UserModel { $dto=$this->mapper->fromModelToDto($user); $sql='INSERT INTO users (id,name,email,password,role,status,created_at,updated_at) VALUES (:id,:name,:email,:password,:role,:status,NOW(),NOW())'; $st=$this->pdo->prepare($sql); $st->execute([':id'=>$dto->id(),':name'=>$dto->name(),':email'=>$dto->email(),':password'=>$dto->password(),':role'=>$dto->role(),':status'=>$dto->status()]); return $this->getById(new UserId($dto->id())); }
    public function update(UserModel $user): UserModel { $dto=$this->mapper->fromModelToDto($user); $sql='UPDATE users SET name=:name,email=:email,password=:password,role=:role,status=:status,updated_at=NOW() WHERE id=:id'; $st=$this->pdo->prepare($sql); $st->execute([':id'=>$dto->id(),':name'=>$dto->name(),':email'=>$dto->email(),':password'=>$dto->password(),':role'=>$dto->role(),':status'=>$dto->status()]); return $this->getById(new UserId($dto->id())); }
    public function getById(UserId $userId): ?UserModel { $st=$this->pdo->prepare('SELECT id,name,email,password,role,status,created_at,updated_at FROM users WHERE id=:id LIMIT 1'); $st->execute([':id'=>$userId->value()]); $row=$st->fetch(); return $row===false?null:$this->mapper->fromRowToModel($row); }
    public function getByEmail(UserEmail $email): ?UserModel { $st=$this->pdo->prepare('SELECT id,name,email,password,role,status,created_at,updated_at FROM users WHERE email=:email LIMIT 1'); $st->execute([':email'=>$email->value()]); $row=$st->fetch(); return $row===false?null:$this->mapper->fromRowToModel($row); }
    public function getAll(): array { $rows=$this->pdo->query('SELECT id,name,email,password,role,status,created_at,updated_at FROM users ORDER BY name ASC')->fetchAll(); return $this->mapper->fromRowsToModels($rows); }
    public function delete(UserId $userId): void { $st=$this->pdo->prepare('DELETE FROM users WHERE id=:id'); $st->execute([':id'=>$userId->value()]); }
    public function updatePassword(UserId $userId, UserPassword $password): void { $st=$this->pdo->prepare('UPDATE users SET password=:password, updated_at=NOW() WHERE id=:id'); $st->execute([':id'=>$userId->value(), ':password'=>$password->value()]); }
}
''')

# Vehiculo infra
add('Infrastructure/Adapters/Persistence/MySQL/Dto/VehiculoPersistenceDto.php', '''<?php
declare(strict_types=1);
final class VehiculoPersistenceDto { private array $data; public function __construct(array $data){$this->data=$data;} public function all(): array { return $this->data; } }
''')
add('Infrastructure/Adapters/Persistence/MySQL/Mapper/VehiculoPersistenceMapper.php', '''
<?php
declare(strict_types=1);
final class VehiculoPersistenceMapper
{
    public function fromModelToDto(VehiculoModel $v): VehiculoPersistenceDto { return new VehiculoPersistenceDto(['id'=>$v->id()->value(),'placa'=>$v->placa()->value(),'marca'=>$v->marca()->value(),'modelo'=>$v->modelo()->value(),'version'=>$v->version()->value(),'color'=>$v->color()->value(),'numPuestos'=>$v->numPuestos()->value(),'numPuertas'=>$v->numPuertas()->value(),'combustible'=>$v->combustible()->value(),'kilometros'=>$v->kilometros()->value(),'cilindraje'=>$v->cilindraje()->value(),'categoria'=>$v->categoria()->value()]); }
    public function fromRowToModel(array $row): VehiculoModel { return new VehiculoModel(new VehiculoId((string)$row['id']),new VehiculoPlaca((string)$row['placa']),new VehiculoTexto((string)$row['marca'],'marca'),new VehiculoTexto((string)$row['modelo'],'modelo'),new VehiculoTexto((string)$row['version'],'version'),new VehiculoTexto((string)$row['color'],'color'),new VehiculoNumero((int)$row['num_puestos'],'numPuestos'),new VehiculoNumero((int)$row['num_puertas'],'numPuertas'),new VehiculoTexto((string)$row['combustible'],'combustible'),new VehiculoNumero((int)$row['kilometros'],'kilometros'),new VehiculoNumero((int)$row['cilindraje'],'cilindraje'),new VehiculoTexto((string)$row['categoria'],'categoria')); }
    public function fromRowsToModels(array $rows): array { return array_map(fn($row)=>$this->fromRowToModel($row), $rows); }
}
''')
add('Infrastructure/Adapters/Persistence/MySQL/Repository/VehiculoRepositoryMySQL.php', '''
<?php
declare(strict_types=1);
final class VehiculoRepositoryMySQL implements SaveVehiculoPort, UpdateVehiculoPort, GetVehiculoByIdPort, GetVehiculoByPlacaPort, GetAllVehiculosPort, DeleteVehiculoPort
{
    private PDO $pdo; private VehiculoPersistenceMapper $mapper;
    public function __construct(PDO $pdo, VehiculoPersistenceMapper $mapper){$this->pdo=$pdo;$this->mapper=$mapper;}
    public function save(VehiculoModel $vehiculo): VehiculoModel { $d=$this->mapper->fromModelToDto($vehiculo)->all(); $sql='INSERT INTO vehiculos (id,placa,marca,modelo,version,color,num_puestos,num_puertas,combustible,kilometros,cilindraje,categoria,created_at,updated_at) VALUES (:id,:placa,:marca,:modelo,:version,:color,:numPuestos,:numPuertas,:combustible,:kilometros,:cilindraje,:categoria,NOW(),NOW())'; $st=$this->pdo->prepare($sql); $st->execute([':id'=>$d['id'],':placa'=>$d['placa'],':marca'=>$d['marca'],':modelo'=>$d['modelo'],':version'=>$d['version'],':color'=>$d['color'],':numPuestos'=>$d['numPuestos'],':numPuertas'=>$d['numPuertas'],':combustible'=>$d['combustible'],':kilometros'=>$d['kilometros'],':cilindraje'=>$d['cilindraje'],':categoria'=>$d['categoria']]); return $this->getById(new VehiculoId($d['id'])); }
    public function update(VehiculoModel $vehiculo): VehiculoModel { $d=$this->mapper->fromModelToDto($vehiculo)->all(); $sql='UPDATE vehiculos SET placa=:placa,marca=:marca,modelo=:modelo,version=:version,color=:color,num_puestos=:numPuestos,num_puertas=:numPuertas,combustible=:combustible,kilometros=:kilometros,cilindraje=:cilindraje,categoria=:categoria,updated_at=NOW() WHERE id=:id'; $st=$this->pdo->prepare($sql); $st->execute([':id'=>$d['id'],':placa'=>$d['placa'],':marca'=>$d['marca'],':modelo'=>$d['modelo'],':version'=>$d['version'],':color'=>$d['color'],':numPuestos'=>$d['numPuestos'],':numPuertas'=>$d['numPuertas'],':combustible'=>$d['combustible'],':kilometros'=>$d['kilometros'],':cilindraje'=>$d['cilindraje'],':categoria'=>$d['categoria']]); return $this->getById(new VehiculoId($d['id'])); }
    public function getById(VehiculoId $vehiculoId): ?VehiculoModel { $st=$this->pdo->prepare('SELECT * FROM vehiculos WHERE id=:id LIMIT 1'); $st->execute([':id'=>$vehiculoId->value()]); $row=$st->fetch(); return $row===false?null:$this->mapper->fromRowToModel($row); }
    public function getByPlaca(VehiculoPlaca $placa): ?VehiculoModel { $st=$this->pdo->prepare('SELECT * FROM vehiculos WHERE placa=:placa LIMIT 1'); $st->execute([':placa'=>$placa->value()]); $row=$st->fetch(); return $row===false?null:$this->mapper->fromRowToModel($row); }
    public function getAll(): array { $rows=$this->pdo->query('SELECT * FROM vehiculos ORDER BY marca ASC, modelo ASC')->fetchAll(); return $this->mapper->fromRowsToModels($rows); }
    public function delete(VehiculoId $vehiculoId): void { $st=$this->pdo->prepare('DELETE FROM vehiculos WHERE id=:id'); $st->execute([':id'=>$vehiculoId->value()]); }
}
''')

# Web/presentation
add('Infrastructure/Entrypoints/Web/Config/WebRoutes.php', '''
<?php
declare(strict_types=1);
final class WebRoutes
{
    public static function all(): array
    {
        return [
            'home' => ['GET', 'home'],
            'auth.login' => ['GET', 'auth.login'],
            'auth.authenticate' => ['POST', 'auth.authenticate'],
            'auth.logout' => ['POST', 'auth.logout'],
            'auth.forgot' => ['GET', 'auth.forgot'],
            'auth.sendForgot' => ['POST', 'auth.sendForgot'],
            'users.index' => ['GET', 'users.index'],
            'users.create' => ['GET', 'users.create'],
            'users.store' => ['POST', 'users.store'],
            'users.show' => ['GET', 'users.show'],
            'users.edit' => ['GET', 'users.edit'],
            'users.update' => ['POST', 'users.update'],
            'users.delete' => ['POST', 'users.delete'],
            'vehiculos.index' => ['GET', 'vehiculos.index'],
            'vehiculos.create' => ['GET', 'vehiculos.create'],
            'vehiculos.store' => ['POST', 'vehiculos.store'],
            'vehiculos.show' => ['GET', 'vehiculos.show'],
            'vehiculos.edit' => ['GET', 'vehiculos.edit'],
            'vehiculos.update' => ['POST', 'vehiculos.update'],
            'vehiculos.delete' => ['POST', 'vehiculos.delete'],
        ];
    }
}
''')
add('Infrastructure/Entrypoints/Web/controllers/UserController.php', '''
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
''')
add('Infrastructure/Entrypoints/Web/controllers/AuthController.php', '''
<?php
declare(strict_types=1);
final class AuthController
{
    public function authenticate(array $post): void { $user = DependencyInjection::getLoginUseCase()->execute(new LoginCommand($post['email'] ?? '', $post['password'] ?? '')); $_SESSION['auth'] = ['id'=>$user->id()->value(),'name'=>$user->name()->value(),'email'=>$user->email()->value(),'role'=>$user->role()]; Flash::set('success', 'Bienvenido, ' . $user->name()->value() . '.'); View::redirect('home'); }
    public function logout(): void { $_SESSION = []; session_destroy(); session_start(); Flash::set('success', 'Sesión cerrada correctamente.'); View::redirect('auth.login'); }
    public function forgot(array $post): void { DependencyInjection::getForgotPasswordUseCase()->execute(new ForgotPasswordCommand($post['email'] ?? '')); Flash::set('success', 'Si el correo existe, se envió una contraseña temporal.'); View::redirect('auth.login'); }
}
''')
add('Infrastructure/Entrypoints/Web/controllers/VehiculoController.php', '''
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
''')
add('Presentation/View.php', '''
<?php
declare(strict_types=1);
final class View
{
    public static function render(string $template, array $data = []): void
    {
        extract($data);
        $flash = Flash::all();
        require dirname(__DIR__) . '/Presentation/Views/' . $template . '.php';
    }
    public static function redirect(string $route): void
    {
        header('Location: index.php?route=' . $route);
        exit;
    }
}
''')
add('Presentation/Flash.php', '''
<?php
declare(strict_types=1);
final class Flash
{
    public static function set(string $key, string $message): void { $_SESSION['_flash'][$key] = $message; }
    public static function all(): array { $flash = $_SESSION['_flash'] ?? []; unset($_SESSION['_flash']); return $flash; }
}
''')

# views
layout_header = '''
<!doctype html>
<html lang="es">
<head>
    <meta charset="utf-8">
    <title>CRUD Hexagonal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; background: #f4f4f4; }
        header, nav, main { padding: 16px; }
        header { background: #222; color: white; }
        nav { background: #eee; display:flex; gap:12px; align-items:center; flex-wrap:wrap; }
        a { color: #0a58ca; text-decoration: none; }
        table { width: 100%; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align:left; }
        form.inline { display:inline; }
        .container { max-width: 1100px; margin: 0 auto; }
        .card { background:white; padding:16px; margin:16px 0; }
        .flash-success { background:#d1e7dd; padding:10px; margin:12px 0; }
        .flash-error { background:#f8d7da; padding:10px; margin:12px 0; }
        input, select { width:100%; padding:8px; margin:6px 0 12px; }
        button { padding:8px 14px; }
        .grid { display:grid; grid-template-columns: 1fr 1fr; gap: 16px; }
    </style>
</head>
<body>
<header><div class="container"><h1>CRUD Hexagonal PHP + MySQL</h1></div></header>
<nav><div class="container">
    <a href="index.php?route=home">Inicio</a>
    <?php if (isset($_SESSION['auth']['id'])): ?>
        <a href="index.php?route=users.index">Usuarios</a>
        <a href="index.php?route=vehiculos.index">Vehículos</a>
        <span>Sesión: <?= htmlspecialchars($_SESSION['auth']['name']) ?></span>
        <form class="inline" method="post" action="index.php?route=auth.logout"><button type="submit">Salir</button></form>
    <?php else: ?>
        <a href="index.php?route=auth.login">Iniciar sesión</a>
    <?php endif; ?>
</div></nav>
<main><div class="container">
<?php foreach ($flash as $type => $message): ?>
    <div class="flash-<?= htmlspecialchars($type) ?>"><?= htmlspecialchars($message) ?></div>
<?php endforeach; ?>
'''
layout_footer = '''
</div></main>
</body>
</html>
'''
add('Presentation/Views/layouts/header.php', layout_header)
add('Presentation/Views/layouts/footer.php', layout_footer)
add('Presentation/Views/home.php', '''
<?php require __DIR__ . '/layouts/header.php'; ?>
<div class="card">
    <h2>Inicio</h2>
    <p>Proyecto base con arquitectura hexagonal, DDD y CQRS.</p>
    <p>Incluye CRUD de usuarios, inicio de sesión, recuperación de contraseña y CRUDL de vehículos.</p>
</div>
<?php require __DIR__ . '/layouts/footer.php'; ?>
''')
add('Presentation/Views/auth/login.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card">
    <h2>Iniciar sesión</h2>
    <form method="post" action="index.php?route=auth.authenticate">
        <label>Correo</label><input type="email" name="email" required>
        <label>Contraseña</label><input type="password" name="password" required>
        <button type="submit">Ingresar</button>
    </form>
    <p><a href="index.php?route=auth.forgot">¿Olvidaste tu contraseña?</a></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/auth/forgot.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card">
    <h2>Recuperar contraseña</h2>
    <form method="post" action="index.php?route=auth.sendForgot">
        <label>Correo</label><input type="email" name="email" required>
        <button type="submit">Enviar contraseña temporal</button>
    </form>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/emails/forgot-password.php', '''
<!doctype html>
<html lang="es"><body>
<h2>Recuperación de contraseña</h2>
<p>Hola <?= htmlspecialchars($name) ?>,</p>
<p>Se ha generado una contraseña temporal para tu cuenta <?= htmlspecialchars($email) ?>.</p>
<p><strong>Contraseña temporal:</strong> <?= htmlspecialchars($temporaryPassword) ?></p>
<p>Inicia sesión y luego cambia la contraseña desde el módulo de usuarios.</p>
</body></html>
''')
# user views
add('Presentation/Views/users/list.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Usuarios</h2><p><a href="index.php?route=users.create">Crear usuario</a></p>
<table><thead><tr><th>Nombre</th><th>Email</th><th>Rol</th><th>Estado</th><th>Acciones</th></tr></thead><tbody>
<?php foreach ($users as $user): ?>
<tr>
<td><?= htmlspecialchars($user->name()->value()) ?></td>
<td><?= htmlspecialchars($user->email()->value()) ?></td>
<td><?= htmlspecialchars($user->role()) ?></td>
<td><?= htmlspecialchars($user->status()) ?></td>
<td>
<a href="index.php?route=users.show&id=<?= urlencode($user->id()->value()) ?>">Ver</a> |
<a href="index.php?route=users.edit&id=<?= urlencode($user->id()->value()) ?>">Editar</a> |
<form class="inline" method="post" action="index.php?route=users.delete"><input type="hidden" name="id" value="<?= htmlspecialchars($user->id()->value()) ?>"><button type="submit">Eliminar</button></form>
</td></tr>
<?php endforeach; ?>
</tbody></table></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/users/create.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Crear usuario</h2><form method="post" action="index.php?route=users.store">
<label>Nombre</label><input name="name" required>
<label>Email</label><input type="email" name="email" required>
<label>Contraseña</label><input type="password" name="password" required>
<label>Rol</label><select name="role"><option>ADMIN</option><option selected>MEMBER</option><option>REVIEWER</option></select>
<button type="submit">Guardar</button>
</form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/users/show.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Detalle de usuario</h2>
<p><strong>ID:</strong> <?= htmlspecialchars($user->id()->value()) ?></p>
<p><strong>Nombre:</strong> <?= htmlspecialchars($user->name()->value()) ?></p>
<p><strong>Email:</strong> <?= htmlspecialchars($user->email()->value()) ?></p>
<p><strong>Rol:</strong> <?= htmlspecialchars($user->role()) ?></p>
<p><strong>Estado:</strong> <?= htmlspecialchars($user->status()) ?></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/users/edit.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Editar usuario</h2><form method="post" action="index.php?route=users.update">
<input type="hidden" name="id" value="<?= htmlspecialchars($user->id()->value()) ?>">
<label>Nombre</label><input name="name" value="<?= htmlspecialchars($user->name()->value()) ?>" required>
<label>Email</label><input type="email" name="email" value="<?= htmlspecialchars($user->email()->value()) ?>" required>
<label>Nueva contraseña</label><input type="password" name="password">
<label>Rol</label><select name="role"><?php foreach (UserRoleEnum::values() as $role): ?><option value="<?= htmlspecialchars($role) ?>" <?= $role === $user->role() ? 'selected' : '' ?>><?= htmlspecialchars($role) ?></option><?php endforeach; ?></select>
<label>Estado</label><select name="status"><?php foreach (UserStatusEnum::values() as $status): ?><option value="<?= htmlspecialchars($status) ?>" <?= $status === $user->status() ? 'selected' : '' ?>><?= htmlspecialchars($status) ?></option><?php endforeach; ?></select>
<button type="submit">Actualizar</button>
</form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
# vehiculo views
veh_form = '''
<div class="grid">
<div><label>Placa</label><input name="placa" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->placa()->value()) : '' ?>" required></div>
<div><label>Marca</label><input name="marca" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->marca()->value()) : '' ?>" required></div>
<div><label>Modelo</label><input name="modelo" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->modelo()->value()) : '' ?>" required></div>
<div><label>Versión</label><input name="version" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->version()->value()) : '' ?>" required></div>
<div><label>Color</label><input name="color" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->color()->value()) : '' ?>" required></div>
<div><label>Número de puestos</label><input type="number" min="1" name="numPuestos" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->numPuestos()->value()) : '' ?>" required></div>
<div><label>Número de puertas</label><input type="number" min="1" name="numPuertas" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->numPuertas()->value()) : '' ?>" required></div>
<div><label>Combustible</label><input name="combustible" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->combustible()->value()) : '' ?>" required></div>
<div><label>Kilómetros</label><input type="number" min="0" name="kilometros" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->kilometros()->value()) : '' ?>" required></div>
<div><label>Cilindraje</label><input type="number" min="0" name="cilindraje" value="<?= isset($vehiculo) ? htmlspecialchars((string) $vehiculo->cilindraje()->value()) : '' ?>" required></div>
<div><label>Categoría</label><input name="categoria" value="<?= isset($vehiculo) ? htmlspecialchars($vehiculo->categoria()->value()) : '' ?>" required></div>
</div>
'''
add('Presentation/Views/vehiculos/list.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Vehículos</h2><p><a href="index.php?route=vehiculos.create">Crear vehículo</a></p>
<table><thead><tr><th>Placa</th><th>Marca</th><th>Modelo</th><th>Categoría</th><th>Color</th><th>Acciones</th></tr></thead><tbody>
<?php foreach ($vehiculos as $vehiculo): ?>
<tr>
<td><?= htmlspecialchars($vehiculo->placa()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->marca()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->modelo()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->categoria()->value()) ?></td>
<td><?= htmlspecialchars($vehiculo->color()->value()) ?></td>
<td>
<a href="index.php?route=vehiculos.show&id=<?= urlencode($vehiculo->id()->value()) ?>">Ver</a> |
<a href="index.php?route=vehiculos.edit&id=<?= urlencode($vehiculo->id()->value()) ?>">Editar</a> |
<form class="inline" method="post" action="index.php?route=vehiculos.delete"><input type="hidden" name="id" value="<?= htmlspecialchars($vehiculo->id()->value()) ?>"><button type="submit">Eliminar</button></form>
</td></tr>
<?php endforeach; ?>
</tbody></table></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/vehiculos/create.php', f'''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Crear vehículo</h2><form method="post" action="index.php?route=vehiculos.store">{veh_form}<button type="submit">Guardar</button></form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/vehiculos/edit.php', f'''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Editar vehículo</h2><form method="post" action="index.php?route=vehiculos.update"><input type="hidden" name="id" value="<?= htmlspecialchars($vehiculo->id()->value()) ?>">{veh_form}<button type="submit">Actualizar</button></form></div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')
add('Presentation/Views/vehiculos/show.php', '''
<?php require __DIR__ . '/../layouts/header.php'; ?>
<div class="card"><h2>Detalle de vehículo</h2>
<p><strong>ID:</strong> <?= htmlspecialchars($vehiculo->id()->value()) ?></p>
<p><strong>Placa:</strong> <?= htmlspecialchars($vehiculo->placa()->value()) ?></p>
<p><strong>Marca:</strong> <?= htmlspecialchars($vehiculo->marca()->value()) ?></p>
<p><strong>Modelo:</strong> <?= htmlspecialchars($vehiculo->modelo()->value()) ?></p>
<p><strong>Versión:</strong> <?= htmlspecialchars($vehiculo->version()->value()) ?></p>
<p><strong>Color:</strong> <?= htmlspecialchars($vehiculo->color()->value()) ?></p>
<p><strong>Puestos:</strong> <?= htmlspecialchars((string) $vehiculo->numPuestos()->value()) ?></p>
<p><strong>Puertas:</strong> <?= htmlspecialchars((string) $vehiculo->numPuertas()->value()) ?></p>
<p><strong>Combustible:</strong> <?= htmlspecialchars($vehiculo->combustible()->value()) ?></p>
<p><strong>Kilómetros:</strong> <?= htmlspecialchars((string) $vehiculo->kilometros()->value()) ?></p>
<p><strong>Cilindraje:</strong> <?= htmlspecialchars((string) $vehiculo->cilindraje()->value()) ?></p>
<p><strong>Categoría:</strong> <?= htmlspecialchars($vehiculo->categoria()->value()) ?></p>
</div>
<?php require __DIR__ . '/../layouts/footer.php'; ?>
''')

# public index
add('public/index.php', '''
<?php
declare(strict_types=1);

session_start();

$projectRoot = dirname(__DIR__);
require_once $projectRoot . '/Common/DependencyInjection.php';
DependencyInjection::bootstrap($projectRoot);

$route = $_GET['route'] ?? 'home';
$routes = WebRoutes::all();
if (!isset($routes[$route])) {
    http_response_code(404);
    echo 'Ruta no encontrada';
    exit;
}
[$expectedMethod, $action] = $routes[$route];
if ($_SERVER['REQUEST_METHOD'] !== $expectedMethod) {
    http_response_code(405);
    echo 'Método no permitido';
    exit;
}

$publicRoutes = ['home', 'auth.login', 'auth.authenticate', 'auth.forgot', 'auth.sendForgot'];
if (!in_array($route, $publicRoutes, true) && !isset($_SESSION['auth']['id'])) {
    Flash::set('error', 'Debes iniciar sesión.');
    View::redirect('auth.login');
}

try {
    switch ($action) {
        case 'home': View::render('home'); break;
        case 'auth.login': View::render('auth/login'); break;
        case 'auth.forgot': View::render('auth/forgot'); break;
        case 'auth.authenticate': (new AuthController())->authenticate($_POST); break;
        case 'auth.logout': (new AuthController())->logout(); break;
        case 'auth.sendForgot': (new AuthController())->forgot($_POST); break;
        case 'users.index': View::render('users/list', (new UserController())->index()); break;
        case 'users.create': View::render('users/create'); break;
        case 'users.store': (new UserController())->store($_POST); break;
        case 'users.show': View::render('users/show', (new UserController())->show($_GET['id'] ?? '')); break;
        case 'users.edit': View::render('users/edit', (new UserController())->show($_GET['id'] ?? '')); break;
        case 'users.update': (new UserController())->update($_POST); break;
        case 'users.delete': (new UserController())->delete($_POST); break;
        case 'vehiculos.index': View::render('vehiculos/list', (new VehiculoController())->index()); break;
        case 'vehiculos.create': View::render('vehiculos/create'); break;
        case 'vehiculos.store': (new VehiculoController())->store($_POST); break;
        case 'vehiculos.show': View::render('vehiculos/show', (new VehiculoController())->show($_GET['id'] ?? '')); break;
        case 'vehiculos.edit': View::render('vehiculos/edit', (new VehiculoController())->show($_GET['id'] ?? '')); break;
        case 'vehiculos.update': (new VehiculoController())->update($_POST); break;
        case 'vehiculos.delete': (new VehiculoController())->delete($_POST); break;
    }
} catch (Throwable $e) {
    Flash::set('error', $e->getMessage());
    $fallback = isset($_SESSION['auth']['id']) ? 'home' : 'auth.login';
    header('Location: index.php?route=' . $fallback);
}
''')

# SQL and readme
add('database.sql', '''
CREATE DATABASE IF NOT EXISTS crud_vehiculos;
USE crud_vehiculos;

CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(36) NOT NULL,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(30) NOT NULL,
    status VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_users_email (email)
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id VARCHAR(36) NOT NULL,
    placa VARCHAR(10) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    modelo VARCHAR(30) NOT NULL,
    version VARCHAR(50) NOT NULL,
    color VARCHAR(30) NOT NULL,
    num_puestos INT NOT NULL,
    num_puertas INT NOT NULL,
    combustible VARCHAR(20) NOT NULL,
    kilometros INT NOT NULL,
    cilindraje INT NOT NULL,
    categoria VARCHAR(30) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uk_vehiculos_placa (placa)
);

INSERT INTO users (id, name, email, password, role, status, created_at, updated_at)
VALUES (
    'admin-seed-001',
    'Administrador',
    'admin@demo.com',
    '$2y$10$CAqN/fQDDJp7s5xX9U.BdufQqsOoC1M72gYPmWaWQXwXJrmsRiyJq',
    'ADMIN',
    'ACTIVE',
    NOW(),
    NOW()
);
-- contraseña: Admin123*
''')
add('README.md', '''
# CRUD Hexagonal PHP + MySQL

Proyecto base alineado con las guías del curso:
- Arquitectura hexagonal
- DDD
- CQRS
- CRUD de usuarios
- Login
- Recuperación de contraseña por correo
- CRUDL de vehículos

## Instalación
1. Importa `database.sql` en MySQL.
2. Ajusta `config/database.php`.
3. Sirve la carpeta del proyecto en Apache/Laragon/XAMPP.
4. Abre `public/index.php`.

## Credenciales de prueba
- Correo: `admin@demo.com`
- Contraseña: `Admin123*`

## Ramas sugeridas
- feature/guia-crud-usuarios
- feature/login
- feature/recuperacion-password
- feature/crudl-vehiculo
- docs/pdf-entrega
''')

for path, content in files.items():
    file_path = base / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.write_text(content, encoding='utf-8')

print(f'Wrote {len(files)} files')
