import { ApiService } from "../api";

export default class DataSourceService {
  #api;
  #baseUrl = '/data-source'

  constructor(api: ApiService) {
    this.#api = api;
  }

  getDataSource(id: string) {
    return this.#api.get(this.#baseUrl, { searchParams: { id } });
  }

  getDataSources() {
    return this.#api.get(this.#baseUrl);
  }
}
