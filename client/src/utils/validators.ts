export const required = <T,>(key: string, model: T) =>
  ((value) => value ? true : { key, value, message: 'This field is required' })(model[key as keyof T]);

export const Same = (field: string, message?: string) => <T,>(key: string, model: T) =>
  ((value1, value2) => value1 === value2 ? true : { key, value: value1, message: message||`Value is not equal to ${field} value` })(model[key as keyof T], model[field as keyof T]);

export const email = <T,>(key: string, model: T) =>
  ((value: string) => value.match(/^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i) ? true : { key, value, message: 'Not valid email' })(model[key as keyof T] as string);

export const AnyRequired = (fields: string[], message?: string) => <T,>(key: string, model: T) =>
  (
    (keys: string[]) => keys.map(field => model[field as keyof T]).filter(value => !!value).length ||
      { key, value: model[key as keyof T], message: message || `At least one of ${fields.join(', ')} fields is required` }
  )([...fields, key]);
