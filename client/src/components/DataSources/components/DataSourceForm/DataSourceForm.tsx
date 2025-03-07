import {
  FileUploader,
  Form,
  Select,
  SelectItem,
  TextInput,
  Toggle,
} from "@carbon/react";
import { ChangeEvent, useState } from "react";
import { ValidationErrors } from "../../../../modules/validation/types";

import "./DataSourceForm.scss";

type DataSourceType = "FILE" | "POSTGRES" | "MYSQL" | "S3";

export interface DataSourceFormModel {
  pk?: number;
  name?: string;
  source_type?: DataSourceType;
  upload?: File;
  header?: boolean;
  host?: string;
  port?: string;
  database?: string;
  user?: string;
  password?: string;
  table?: string;
  query?: string;
}

interface ConfigItem {
  key: string;
  label: string;
}

interface DataSourceFormProps {
  model?: DataSourceFormModel;
  onChange?: (model: DataSourceFormModel) => void;
  edit?: boolean;
  errors?: ValidationErrors;
}

export default function DataSourceForm({
  model = {},
  onChange,
  edit,
  errors,
}: DataSourceFormProps) {
  const [state, setState] = useState({
    source_type: "FILE",
    ...model,
  } as DataSourceFormModel);

  const HandleChange =
    <T,>(setter: (event: ChangeEvent<T>) => void) =>
    (event: ChangeEvent<T>) => {
      setter(event);
      onChange?.(state);
    };

  const handleNameChange = HandleChange<HTMLInputElement>((event) => {
    setState({ ...state, name: event.target.value });
  });

  const handleSourceTypeChange = HandleChange<HTMLSelectElement>((event) => {
    setState({ ...state, source_type: event.target.value as DataSourceType });
  });

  const handleFileChange = HandleChange<HTMLInputElement>((event) => {
    setState({
      ...state,
      upload: event.target.files?.[0],
      header: !state.upload?.name.endsWith(".csv"),
    });
  });

  const handleHeaderChange = (checked: boolean) => {
    setState({ ...state, header: checked });
    onChange?.(state);
  };

  const HandleConfigChange = (key: keyof DataSourceFormModel) =>
    HandleChange<HTMLInputElement>((event) => {
      console.log(key, event.target.value);
      setState({
        ...state,
        [key]: event.target.value,
      });
    });

  const MYSQL_POSGRES_CONFIG: ConfigItem[] = [
    { key: "host", label: "Host" },
    { key: "port", label: "Port" },
    { key: "database", label: "Database" },
    { key: "user", label: "User" },
    { key: "password", label: "Password" },
    { key: "table", label: "Table" },
    { key: "query", label: "Query" },
  ];

  return (
    <Form className="data-source-form">
      <TextInput
        id="name"
        labelText="Name"
        value={model.name}
        warn={!!errors?.name}
        warnText={errors?.name?.message}
        onChange={handleNameChange}
      />
      {!edit && (
        <>
          <Select
            id="sourceType"
            labelText="Type"
            value={model.source_type}
            onChange={handleSourceTypeChange}
          >
            <SelectItem value="FILE" text="File" />
            <SelectItem value="POSTGRES" text="PostgreSQL" />
            <SelectItem value="MYSQL" text="MySQL" />
            <SelectItem value="S3" text="S3 Bucket" />
          </Select>
          {state.source_type === "FILE" && (
            <>
              <FileUploader
                filenameStatus="edit"
                name="upload"
                accept={[".csv", ".xls", ".xlsx"]}
                labelTitle="Upload file"
                size="md"
                labelDescription="Max file size is 50 MB. Only .csv, .xls, xlsx files are supported."
                onChange={handleFileChange}
              />
              {state.upload?.name.endsWith(".csv") && (
                <Toggle
                  id="header"
                  labelA="exclude headers"
                  labelB="include headers"
                  onToggle={handleHeaderChange}
                />
              )}
            </>
          )}
          {["POSTGRES", "MYSQL"].includes(state.source_type!) && (
            <>
              {MYSQL_POSGRES_CONFIG.map((item: ConfigItem) => (
                <TextInput
                  id={`config.${item.key}`}
                  labelText={item.label}
                  value={model[item.key as keyof DataSourceFormModel] as string}
                  warn={!!errors?.[item.key]}
                  warnText={errors?.[item.key]?.message}
                  onChange={HandleConfigChange(
                    item.key as keyof DataSourceFormModel,
                  )}
                />
              ))}
            </>
          )}
        </>
      )}
    </Form>
  );
}
