import { ResponsePromise } from "ky";
import { DataSource } from "../../components/DataSources/types";
import { ApiService } from "../api";

export default class DataSourceService {
  #api;
  #baseUrl = 'datasources';

  constructor(api: ApiService) {
    this.#api = api;
  }

  getDataSource(pk: string): ResponsePromise<DataSource> {
    return this.#api.get(this.#baseUrl, { searchParams: { pk } });
  }

  getDataSources(): ResponsePromise<DataSource[]> {
    return this.#api.get(this.#baseUrl);
  }

  postDataSource(formData: FormData) {
    return this.#api.post(`${this.#baseUrl}/create/`, {
      body: formData
    })
  }

  patchDataSource(pk: number, formData: FormData) {
    return this.#api.patch(`${this.#baseUrl}/${pk}/`, {
      body: formData
    })
  }

  deleteDataSource(pk: number) {
    return this.#api.delete(`${this.#baseUrl}/${pk}/`)
  }
}
