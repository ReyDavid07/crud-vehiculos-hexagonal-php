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
