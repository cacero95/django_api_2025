export interface LoginForm {
    email: string
    password: string
}

export interface RegisterForm extends LoginForm {
    name: string
    last_name: string
}

export interface LoginResponse {
    status:   boolean;
    message:  string;
    token:    string;
    username: string;
    name:     string;
}