import { KyInstance, Options } from 'ky';

export default class ApiService {
  #ky: KyInstance;

  constructor(ky: KyInstance) {
    this.#ky = ky.create({
      headers: {},
      hooks: {
        beforeRequest: [
          () => console.log('before')
        ]
      },
      prefixUrl: ''
    })
  }

  get(url: string, options: Options = {}) {
    return this.#ky.get(url, options);
  }
}
