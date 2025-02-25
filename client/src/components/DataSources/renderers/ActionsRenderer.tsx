import { Edit, TrashCan } from "@carbon/icons-react";
import { Button } from "@carbon/react";
import { ModalController } from "../../common/Modal/Modal";
import { DataSource, ExtendedRendererProps } from "../types";

export interface ActionsRendererProps {
  editModalController: ModalController<DataSource>
  deleteModalController: ModalController<DataSource>
}

export default function ActionsRenderer(props: ExtendedRendererProps<ActionsRendererProps>) {
  const handleDeleteClick = () => {
    props.deleteModalController.open(props.dataSource);
  }

  const handleEditClick = () => {
    props.editModalController.open(props.dataSource);
  }
  return <><div className="etlm-data-source-actions">
    <Button kind="ghost" renderIcon={Edit} iconDescription="Edit Data Source" hasIconOnly onClick={handleEditClick} />
    <Button kind="danger--ghost" renderIcon={TrashCan} iconDescription="Delete Data Source" hasIconOnly onClick={handleDeleteClick} />
  </div></>
}
