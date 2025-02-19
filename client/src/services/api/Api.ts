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
      prefixUrl: import.meta.env.VITE_APP_BASE_URL
    })
  }

  get(url: string, options: Options = {}) {
    return this.#ky.get(url, options);
  }

  post(url: string, options: Options = {}) {
    return this.#ky.post(url, options);
  }
}
