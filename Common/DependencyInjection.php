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
