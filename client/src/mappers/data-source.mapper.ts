import { DataSourceFormModel } from "../components/DataSources/components/DataSourceForm/DataSourceForm";

export const createModelToFormData: (model: DataSourceFormModel) => FormData = (model: DataSourceFormModel) => {
  const formData = new FormData();

  ['name', 'source_type', 'upload'].forEach((key: string) => {
    formData.append(key, model[key as keyof DataSourceFormModel]! as string | Blob);
  });

  formData.append('config', JSON.stringify({ options: { header: !!model.header! } }))

  return formData;
}
