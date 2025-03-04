export const required = <T,>(key: string, model: T) =>
  ((value) => value ? true : { key, value, message: 'This field is required' })(model[key as keyof T]);


export const Same = (field: string, message?: string) => <T,>(key: string, model: T) =>
  ((value1, value2) => value1 === value2 ? true : { key, value: value1, message: message||`Value is not equal to ${field} value` })(model[key as keyof T], model[field as keyof T]);

export const email = <T,>(key: string, model: T) =>
  ((value: string) => value.match(/^(([^<>()[\].,;:\s@"]+(\.[^<>()[\].,;:\s@"]+)*)|(".+"))@(([^<>()[\].,;:\s@"]+\.)+[^<>()[\].,;:\s@"]{2,})$/i) ? true : { key, value, message: 'Not valid email' })(model[key as keyof T] as string);
