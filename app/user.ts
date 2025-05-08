export interface User {
    id: number;
    name: string;
    email: string;
    isActive: boolean;
  }
  
  export class UserImpl implements User {
    constructor(
      public id: number,
      public name: string,
      public email: string,
      public isActive: boolean = true
    ) {}
  
    toString(): string {
      return `User(${this.id}): ${this.name} <${this.email}>`;
    }
  }
  