import { DataSourceFormModel } from "../components/DataSources/components/DataSourceForm/DataSourceForm";
import { DataSource } from "../components/DataSources/types";

export const createModelToFormData: (model: DataSourceFormModel) => FormData = (model: DataSourceFormModel) => {
  const formData = new FormData();

  ['name', 'source_type', 'upload'].forEach((key: string) => {
    formData.append(key, model[key as keyof DataSourceFormModel]! as string | Blob);
  });

  formData.append('config', JSON.stringify({ options: { header: !!model.header! } }))

  return formData;
}

export const editModelToFormData: (model: DataSourceFormModel) => FormData = (model: DataSourceFormModel) => {
  const formData = new FormData();

  formData.append('name', model.name as string);

  return formData;
}

export const dataSourceToEditModel: (model: DataSource) => DataSourceFormModel = (model: DataSource) => {
  return {
    pk: model.pk,
    name: model.name,
    source_type: model.source_type
  } as DataSourceFormModel;
}
