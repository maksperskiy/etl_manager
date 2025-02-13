import { Button } from "@carbon/react";
import useModalStore, { ModalAction } from "../../../stores/modal";

import { CloseLarge } from "@carbon/icons-react";
import './ModalProvider.scss';

export default function ModalProvider () {
  const { modals, close } = useModalStore();

  const HandleCloseClick = (id: string) => () => {
    close(id);
  };

  const HandleActionButtonClick = (id: string, action: ModalAction) => () => {
    action.callback?.();

    if (action.close) {
      close(id)
    };
  }

  const handleBackdropClick = () => {
    const lastModal = modals.at(-1);
    if (!lastModal?.persistent) {
      close(lastModal!.id);
    }
  }

  return <>
    <div
      className={['modal__backdrop', ...(modals.length ? ['visible'] : [])].join(' ')}
      onClick={handleBackdropClick}
    />
    {modals.map(modal => <dialog className="modal" open>
      <div className="modal__header">
        <Button
          className="modal__header--close"
          hasIconOnly
          iconDescription="Close"
          kind="ghost"
          renderIcon={CloseLarge}
          onClick={HandleCloseClick(modal.id)}
        />
      </div>
      <div className="modal__body">
        {modal.component}
      </div>
      {
        !!modal.actions.length && <div className="modal__footer">
          {modal.actions.map(action => <Button
            kind={action.kind}
            key={action.key}
            onClick={HandleActionButtonClick(modal.id, action)}
          >
            {action.label}
          </Button>)}
        </div>
      }
    </dialog>)}
  </>
}
