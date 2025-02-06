import apiService from "../api";
import DataSourceService from "./DataSource";

const dataSourceService = new DataSourceService(apiService);

export default dataSourceService;
