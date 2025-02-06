import { Observable } from 'rxjs';
import { Modal } from "./types";

export default class ModalService {
  #modals: Observable<Modal[]> = new Observable()
}
