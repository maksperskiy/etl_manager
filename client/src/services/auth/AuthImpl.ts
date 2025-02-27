import apiService from "../api";
import AuthService from "./Auth";

const authService = new AuthService(apiService);

export default authService;
