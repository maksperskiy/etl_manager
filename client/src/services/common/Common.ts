import { LoginFormModel } from "../../views/Login/Login";
import { RegisterFormModel } from "../../views/Register/Register";
import { ApiService } from "../api";

export default class CommonService {
  #api;
  #baseUrl = 'common';

  constructor(api: ApiService) {
    this.#api = api;
  }

  login(model: LoginFormModel) {
    return this.#api.post(`${this.#baseUrl}/login/`, {
      body: JSON.stringify(model),
      credentials: 'omit'
    })
  }

  register(model: RegisterFormModel) {
    return this.#api.post(`${this.#baseUrl}/signup/`, {
      body: JSON.stringify(model),
      credentials: 'omit'
    })
  }

  logout() {
    return this.#api.post(`${this.#baseUrl}/logout/`)
  }
}
