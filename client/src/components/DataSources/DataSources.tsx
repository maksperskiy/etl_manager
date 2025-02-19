import './DataSources.scss';

import { Add, Save } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useEffect, useState } from 'react';
import useValidation, { Validator } from "../../hooks/useValidation";
import dataSourceService from '../../services/data-source';
import Modal from '../common/Modal/Modal';
import DataSourceForm, { DataSourceFormModel } from './components/DataSourceForm/DataSourceForm';
import DateRenderer from './renderers/DateRenderer';
import { ColumnDef, DataSource } from './types';

import useModalController from '../../hooks/useModalController';
import { required } from '../../utils/validators';

export default function DataSources() {
  const columnDefs: ColumnDef[] = [
    {
      key: 'name',
      label: 'Name',
    },
    {
      key: 'created_at',
      label: 'Loaded',
      renderer: DateRenderer
    },
    {
      key: 'last_used',
      label: 'Last Used',
    },
    {
      key: 'actions',
      label: null,
    }
  ];

  // const { open } = useModalStore();
  const [createModel, setCreateModel] = useState<DataSourceFormModel>({});
  const controller = useModalController();

  const { validate } = useValidation<DataSourceFormModel>({
    name: [required as Validator<DataSourceFormModel>]
  });

  const handleSave = async () => {
    const validationResult = validate(createModel);

    if (validationResult.valid) {
      const timeout = (ms: number) => new Promise(resolve => setTimeout(resolve, ms));
      await timeout(3000);
      controller.close();
    }
  }

  const handleAddClick = () => {
    controller.open();
  }

  const [dataSources, setDataSources] = useState<DataSource[]>([]);

  useEffect(() => {
    (async () => {
      const res = await dataSourceService.getDataSources();
      setDataSources(await res.json());
    })();
  }, [])

  return <div className="etlm-data-sources">
    <Button className="etlm-data-sources__add" renderIcon={Add} onClick={handleAddClick}>Add New Data Source</Button>
    <Modal
      controller={controller}
      title="Add Data Source"
      actions={[
        {
          key: 'cancel',
          label: 'Cancel',
          kind: 'ghost',
          close: true
        },
        {
          key: 'save',
          label: 'Save',
          kind: 'primary',
          close: false,
          icon: Save,
          callback: handleSave
        }
      ]}
    >
      <DataSourceForm onChange={(model) => { setCreateModel(model) }} />
    </Modal>
    <Table aria-label="sample table">
      <TableHead>
        <TableRow>
          {columnDefs.map(def => <TableHeader key={def.key}>{ def.label }</TableHeader>)}
        </TableRow>
      </TableHead>
      <TableBody>
        {dataSources.map(src => <TableRow key={src.name}>
          {columnDefs.map(def => <TableCell  key={def.key}>
            { src[def.key as keyof DataSource] }
          </TableCell>)}
        </TableRow>)}
      </TableBody>
    </Table>
  </div>
}
