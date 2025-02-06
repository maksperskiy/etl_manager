import './DataSources.scss';

import { Add } from '@carbon/icons-react';
import { Button, Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@carbon/react';
import { useState } from 'react';
import DateRenderer from './renderers/DateRenderer';
import { ColumnDef, DataSource } from './types';


export default function DataSources() {
  const columnDefs: ColumnDef[] = [
    {
      key: 'name',
      label: 'Name',
    },
    {
      key: 'dateLoaded',
      label: 'Loaded',
      renderer: DateRenderer
    },
    {
      key: 'dateUsed',
      label: 'Last Used',
    },
    {
      key: 'actions',
      label: null,
    }
  ];

  const [dataSources, setDataSources] = useState([{
    name: 'MacOS',
    type: 'excel',
    dateLoaded: 0,
    dateUsed: 0,
  }]);

  return <div className="etlm-data-sources">
    <Button className="etlm-data-sources__add" renderIcon={Add}>Add New Data Source</Button>
    <Table aria-label="sample table">
      <TableHead>
        <TableRow>
          {columnDefs.map(def => <TableHeader key={def.key}>{ def.label }</TableHeader>)}
        </TableRow>
      </TableHead>
      <TableBody>
        {dataSources.map(src => <TableRow>
          {columnDefs.map(def => <TableCell>
            {
              def.renderer
                ? def.renderer({ dataSource: src, key: def.key })
                : src[def.key as keyof DataSource]
            }
          </TableCell>)}
        </TableRow>)}
      </TableBody>
    </Table>
  </div>
}
