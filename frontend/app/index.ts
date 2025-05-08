import { UserController } from './user-controller';
import { Logger } from './log';

// Main application entry point
const logger = new Logger('App');
logger.info('Application starting');

const userController = new UserController();

// Create some users
const user1 = userController.createUser('Alice Smith', 'alice@example.com');
const user2 = userController.createUser('Bob Johnson', 'bob@example.com');
userController.createUser('Charlie Brown', 'charlie@example.com');

// Get user by ID
const foundUser = userController.getUser(1);
logger.info('Found user:', foundUser);

// List all users
const allUsers = userController.listUsers();
logger.info(`Total users: ${allUsers.length}`);

logger.info('Application ending');
