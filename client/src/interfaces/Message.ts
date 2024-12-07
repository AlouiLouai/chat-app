interface Message {
  username: string;
  message: string;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
}

interface LoginCredentials {
  username: string;
  password: string;
}

interface Tokens {
  access_token: string;
  refresh_token: string;
}

interface ForgotPasswordData {
  email: string;
}

interface ResetPasswordData {
  new_password: string;
}
