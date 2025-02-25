import { CloseLarge } from "@carbon/icons-react";
import { Button, ButtonKind } from '@carbon/react';
import { ElementType, ReactNode, useState } from 'react';

import './Modal.scss';

export type ModalActionCallback = () => Promise<void> | void;

export interface ModalAction {
  key: string
  label: string
  kind: ButtonKind
  callback?: ModalActionCallback
  disabled?: boolean
  close: boolean
  icon?: ElementType
}

export interface ModalController<T> {
  opened: boolean
  open: (buffer?: T) => void
  close: (buffer?: T) => void
  backdrop: (buffer?: T) => void
}

export interface ModalProps<T> {
  title?: string
  children: ReactNode
  actions: ModalAction[],
  controller: ModalController<T>
}

export default function Modal<T> ({ title, children, actions, controller }: ModalProps<T>) {
  const [processing, setProcessing] = useState<boolean>(false);

  const HandleActionButtonClick = (action: ModalAction) => async () => {
    setProcessing(true);
    try {
      await action.callback?.();
    } finally {
      setProcessing(false);
      if (action.close) controller.close();
    }
  }

  const handleClose = () => !processing && controller.close()

  const handleBackdrop = () => !processing && controller.backdrop()

  return controller.opened && <dialog className="modal" open>
    <div className="modal__header">
      {title && <h4>{ title }</h4>}
      <Button
        className="modal__header--close"
        hasIconOnly
        iconDescription="Close"
        kind="ghost"
        renderIcon={CloseLarge}
        onClick={handleClose}
      />
    </div>
    <div className="modal__body">
      {children}
    </div>
    {
      !!actions.length && <div className="modal__footer">
        {actions.map(action => <Button
          kind={action.kind}
          key={action.key}
          disabled={processing || action.disabled}
          onClick={HandleActionButtonClick(action)}
          renderIcon={action.icon}
        >
          {action.label}
        </Button>)}
      </div>
    }
    <div
      className="modal__backdrop"
      onClick={handleBackdrop}
    />
  </dialog>
}
