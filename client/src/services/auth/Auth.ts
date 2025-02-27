import { ApiService } from "../api";

export default class AuthService {
  #api;

  constructor(api: ApiService) {
    this.#api = api;
  }

  login<T>(model: T) {
    return this.#api.post('login', {
      body: JSON.stringify(model)
    })
  }
}
