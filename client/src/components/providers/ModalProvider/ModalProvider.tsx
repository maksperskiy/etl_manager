import { Button } from "@carbon/react";
import useModalStore from "../../../stores/modal";

import { CloseLarge } from "@carbon/icons-react";
import './ModalProvider.scss';

export default function ModalProvider () {
  const { modals, close } = useModalStore();

  const handleCloseClick = (id: string) => () => {
    close(id);
  };

  return <>
    <div className={['modal__backdrop', ...(modals.length ? ['visible'] : [])].join(' ')} />
    {modals.map(modal => <dialog className="modal" open>
      <div className="modal__header">
        <Button
          className="modal__header--close"
          hasIconOnly
          iconDescription="Close"
          kind="ghost"
          renderIcon={CloseLarge}
          onClick={handleCloseClick(modal.id)}
        />
      </div>
      <div className="modal__body">
        {modal.component}
      </div>
      <div className="modal__footer">
        <Button>Save</Button>
      </div>
    </dialog>)}
  </>
}
