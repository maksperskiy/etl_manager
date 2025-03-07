export interface ValidationError {
  key: string;
  value: unknown;
  message: string;
}

export type Validator<T = Record<string, unknown>> = (
  key: string,
  model: T,
) => true | ValidationError;

export interface ValidationSchema<T> {
  [key: string]: Validator<T>[];
}

export interface ValidationErrors {
  [key: string]: ValidationError;
}
