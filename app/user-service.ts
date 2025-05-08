import { User, UserImpl } from './user';
import { Logger } from './log';

export class UserService {
  private users: User[] = [];
  private logger: Logger;

  constructor() {
    this.logger = new Logger('UserService');
    this.logger.info('UserService initialized');
  }

  addUser(name: string, email: string): User {
    const id = this.users.length + 1;
    const user = new UserImpl(id, name, email);
    this.users.push(user);
    this.logger.debug('User added', user);
    return user;
  }

  getUserById(id: number): User | undefined {
    const user = this.users.find(u => u.id === id);
    if (!user) {
      this.logger.warn(`User with id ${id} not found`);
    }
    return user;
  }

  getAllUsers(): User[] {
    return [...this.users];
  }
}
