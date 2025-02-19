import type { Validator } from "../hooks/useValidation";

export const required: Validator = <T,>(key: string, model: T) =>
  ((value) => value ? true : { key, value, message: 'This field is required' })(model[key as keyof T]);
