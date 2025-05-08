
import { UserService } from './user-service';
import { User } from './user';
import { Logger } from './log';

export class UserController {
  private userService: UserService;
  private logger: Logger;

  constructor() {
    this.userService = new UserService();
    this.logger = new Logger('UserController');
  }

  createUser(name: string, email: string): User {
    this.logger.info(`Creating user: ${name}, ${email}`);
    return this.userService.addUser(name, email);
  }

  getUser(id: number): User | undefined {
    this.logger.info(`Fetching user with id: ${id}`);
    return this.userService.getUserById(id);
  }

  listUsers(): User[] {
    this.logger.info('Listing all users');
    return this.userService.getAllUsers();
  }
}
