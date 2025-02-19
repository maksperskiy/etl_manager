
export interface ValidationError {
  key: string
  value: unknown
  message: string
}

export type Validator<T = Record<string, unknown>> = (key: string, model: T) => true | ValidationError;

export interface ValidationSchema<T> {
  [key: string]: Validator<T>[]
}

export interface ValidationErrors {
  [key: string]: ValidationError
}

export default function useValidation<T = Record<string, unknown>>(schema: ValidationSchema<T> = {}) {
  const validate = (model: T) => {
    const errors: ValidationErrors = {};

    Object.keys(schema).forEach((key) => {
      schema[key].find((rule: Validator<T>) => {
        const validatorResult = rule(key, model);
        if (validatorResult !== true) {
          errors[key] = validatorResult;
          return true;
        }
      });
    });

    return {
      valid: Object.keys(errors).length === 0,
      errors,
      model
    }

  };

  return { validate };
}
