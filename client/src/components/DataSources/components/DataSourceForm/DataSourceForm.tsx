import { FileUploader, Form, Select, SelectItem, TextInput, Toggle } from "@carbon/react"
import { ChangeEvent, useState } from "react"

import { Validator } from "../../../../hooks/useValidation"
import { required } from "../../../../utils/validators"
import './DataSourceForm.scss'

type DataSourceType = 'FILE' | 'POSTGRES' | 'MYSQL' | 'S3'

export interface DataSourceFormModel {
  pk?: number
  name?: string
  source_type?: DataSourceType
  upload?: File
  header?: boolean
  config?: {
    host?: string
    port?: string
    database?: string
    user?: string
    password?: string
    table?: string
    quer?: string
  }
}

interface ConfigItem {
  key: string
  validators: Validator[]
  label: string
}

interface DataSourceFormProps {
  model?: DataSourceFormModel
  onChange?: (model: DataSourceFormModel) => void
  edit?: boolean
}

export default function DataSourceForm({ model = {}, onChange, edit }: DataSourceFormProps) {
  const [state, setState] = useState({
    source_type: 'FILE',
    ...model
  } as DataSourceFormModel);

  const HandleChange = <T,>(setter: (event: ChangeEvent<T>) => void) => (event: ChangeEvent<T>) => {
    setter(event);
    onChange?.(state);
  }

  const handleNameChange = HandleChange<HTMLInputElement>(event => {
    setState({ ...state, name: event.target.value });
  });

  const handleSourceTypeChange = HandleChange<HTMLSelectElement>(event => {
    setState({ ...state, source_type: event.target.value as DataSourceType });
  });

  const handleFileChange = HandleChange<HTMLInputElement>(event => {
    setState({
      ...state,
      upload: event.target.files?.[0],
      header: !state.upload?.name.endsWith('.csv')
    });
  });

  const handleHeaderChange = (checked: boolean) => {
    setState({ ...state, header: checked });
    onChange?.(state);
  };

  const HandleConfigChange = (key: keyof DataSourceFormModel['config']) => HandleChange<HTMLInputElement>(event => {
    setState({
      ...state,
      config: {
        ...(state.config || {}),
        [key]: event.target.value
      }
    });
  });

  const MYSQL_POSGRES_CONFIG: ConfigItem[] = [
    { key: 'host', label: 'Host', validators: [required] },
    { key: 'port' },
    { key: 'database' },
    { key: 'user' },
    { key: 'password' },
    { key: 'table' },
    { key: 'query' },
  ];

  return <Form className="data-source-form">
    <TextInput id="name" labelText="Name" value={model.name} onChange={handleNameChange} />
    { !edit && <>
      <Select id="sourceType" labelText="Type" value={model.source_type} onChange={handleSourceTypeChange}>
        <SelectItem value="FILE" text="File" />
        <SelectItem value="POSTGRES" text="PostgreSQL" />
        <SelectItem value="MYSQL" text="MySQL" />
        <SelectItem value="S3" text="S3 Bucket" />
      </Select>
      {
        state.source_type === 'FILE' &&
        <>
          <FileUploader
            filenameStatus="edit"
            name="upload"
            accept={['.csv', '.xls', '.xlsx']}
            labelTitle="Upload file"
            size="md"
            labelDescription="Max file size is 50 MB. Only .csv, .xls, xlsx files are supported."
            onChange={handleFileChange}
          />
          {
            state.upload?.name.endsWith('.csv') &&
            <Toggle id="header" labelA="exclude headers" labelB="include headers" onToggle={handleHeaderChange} />
          }
        </>
      }
      {
        ['POSTGRES', 'MYSQL'].includes(state.source_type!) &&
        <>
          {
            MYSQL_POSGRES_CONFIG.map((item: ConfigItem) => <TextInput
              id={`config.${key}`}
              labelText={key.toUpperCase()}
              value={model.config?.[key as keyof DataSourceFormModel['config']]}
              onChange={HandleConfigChange(key as keyof DataSourceFormModel['config'])}
            />)
          }
        </>
      }
    </> }

  </Form>
}
