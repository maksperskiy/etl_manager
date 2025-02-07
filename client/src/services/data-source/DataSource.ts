import { ResponsePromise } from "ky";
import { DataSource } from "../../components/DataSources/types";
import { ApiService } from "../api";

export default class DataSourceService {
  #api;
  #baseUrl = 'datasources';

  constructor(api: ApiService) {
    this.#api = api;
  }

  getDataSource(id: string): ResponsePromise<DataSource> {
    return this.#api.get(this.#baseUrl, { searchParams: { id } });
  }

  getDataSources(): ResponsePromise<DataSource[]> {
    return this.#api.get(this.#baseUrl);
  }
}
