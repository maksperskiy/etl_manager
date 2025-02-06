import { KyInstance, Options } from 'ky';

export default class ApiService {
  #ky: KyInstance;

  constructor(ky: KyInstance) {
    console.log(import.meta.env.VITE_APP_BASE_URL);

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
}
