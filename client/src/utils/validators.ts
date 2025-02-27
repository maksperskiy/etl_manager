export const required = <T,>(key: string, model: T) =>
  ((value) => value ? true : { key, value, message: 'This field is required' })(model[key as keyof T]);
