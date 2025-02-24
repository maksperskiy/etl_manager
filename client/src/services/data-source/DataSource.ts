import { ResponsePromise } from "ky";
import { DataSourceFormModel } from "../../components/DataSources/components/DataSourceForm/DataSourceForm";
import { DataSource } from "../../components/DataSources/types";
import { createModelToFormData } from "../../mappers/data-source.mapper";
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

  postDataSource(model: DataSourceFormModel) {
    return this.#api.post(`${this.#baseUrl}/create/`, {
      body: createModelToFormData(model)
    })
  }
}
