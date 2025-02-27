import './DataSources.scss';

import { Add, Save, TrashCan } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useEffect, useState } from 'react';
import useValidation from "../../hooks/useValidation";
import dataSourceService from '../../services/data-source';
import Modal from '../common/Modal/Modal';
import DataSourceForm, { DataSourceFormModel } from './components/DataSourceForm/DataSourceForm';
import DateRenderer from './renderers/DateRenderer';
import { ColumnDef, DataSource, ExtendedRendererProps } from './types';

import useModalController from '../../hooks/useModalController';
import { createModelToFormData, dataSourceToEditModel, editModelToFormData } from '../../mappers/data-source.mapper';
import { required } from '../../utils/validators';
import ActionsRenderer, { ActionsRendererProps } from './renderers/ActionsRenderer/ActionsRenderer';

export default function DataSources() {
  const addModalController = useModalController(true);
  const editModalController = useModalController<DataSource>(true);
  const deleteModalController = useModalController<DataSource>(true);

  editModalController.onOpen((dataSource?: DataSource) => {
    if (dataSource) {
      setEditModel(dataSourceToEditModel(dataSource))
    }
  })

  editModalController.onClose(() => {
    setEditModel({});
  })

  deleteModalController.onOpen((dataSource?: DataSource) => {
    setDeleteModel(dataSource!)
  })

  deleteModalController.onClose(() => {
    setDeleteModel(null);
  })

  const [createModel, setCreateModel] = useState<DataSourceFormModel>({});
  const [editModel, setEditModel] = useState<DataSourceFormModel>({});
  const [deleteModel, setDeleteModel] = useState<DataSource | null>(null);

  const columnDefs: ColumnDef<ActionsRendererProps>[] = [
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
      renderer: DateRenderer
    },
    {
      key: 'actions',
      label: null,
      renderer: ActionsRenderer,
      props: { deleteModalController, editModalController },
      class: 'etlm-data-sources__table--actions'
    }
  ];

  const { validate } = useValidation<DataSourceFormModel>({
    name: [required]
  });

  const handleCreate = async () => {
    if (validate(createModel)) {
      await dataSourceService.postDataSource(createModelToFormData(createModel));
      addModalController.close();
      fetchDataSources();
    }
  }

  const handleSave = async () => {
    if (validate(editModel)) {
      await dataSourceService.patchDataSource(editModel.pk!, editModelToFormData(editModel));
      addModalController.close();
      fetchDataSources();
    }
  }

  const handleAddClick = () => {
    addModalController.open();
  }

  const handleDelete = async () => {
    if (deleteModel) {
      await dataSourceService.deleteDataSource(deleteModel.pk);
    }
    deleteModalController.close();
    fetchDataSources();
  }

  const [dataSources, setDataSources] = useState<DataSource[]>([]);

  const fetchDataSources = async () => {
    const res = await dataSourceService.getDataSources();
    setDataSources(await res.json());
  }

  useEffect(() => {
    fetchDataSources();
  }, [])

  return <div className="etlm-data-sources">
    <Button className="etlm-data-sources__add" renderIcon={Add} onClick={handleAddClick}>Add New Data Source</Button>
    <Modal
      controller={addModalController}
      title="Add Data Source"
      actions={[
        {
          key: 'cancel',
          label: 'Cancel',
          kind: 'ghost',
          close: true
        },
        {
          key: 'create',
          label: 'Create',
          kind: 'primary',
          close: false,
          icon: Save,
          callback: handleCreate
        }
      ]}
    >
      <DataSourceForm onChange={(model) => { setCreateModel(model) }} />
    </Modal>
    <Modal
      controller={editModalController}
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
      <DataSourceForm model={editModel} onChange={(model) => { setEditModel(model) }} edit />
    </Modal>
    <Modal
      controller={deleteModalController}
      title="Delete Data Source"
      actions={[
        {
          key: 'cancel',
          label: 'Cancel',
          kind: 'ghost',
          close: true
        },
        {
          key: 'delete',
          label: 'Delete',
          kind: 'danger',
          close: true,
          icon: TrashCan,
          callback: handleDelete
        }
      ]}
    >
      Are you sure you want to delete {<strong>{deleteModel?.name}</strong>}?
    </Modal>
    <Table aria-label="sample table">
      <TableHead>
        <TableRow>
          {columnDefs.map(def => <TableHeader key={def.key}>{ def.label }</TableHeader>)}
        </TableRow>
      </TableHead>
      <TableBody>
        {dataSources.map(src => <TableRow key={src.name}>
          {columnDefs.map(def => <TableCell className={def.class} key={def.key}>
            { def.renderer ? def.renderer({ dataSource: src, key: def.key, ...(def.props || {} as ExtendedRendererProps<ActionsRendererProps>) }) : src[def.key as keyof DataSource] }
          </TableCell>)}
        </TableRow>)}
      </TableBody>
    </Table>
  </div>
}
