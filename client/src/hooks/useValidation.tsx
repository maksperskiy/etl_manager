import { useState } from "react";

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
  const [valid, setValid] = useState<boolean>(true);
  const [errors, setErrors] = useState<ValidationErrors>({});

  const validate = (model: T) => {
    const newErrors: ValidationErrors = {};

    Object.keys(schema).forEach((key) => {
      schema[key].find((rule: Validator<T>) => {
        const validatorResult = rule(key, model);
        if (validatorResult !== true) {
          newErrors[key] = validatorResult;
          return true;
        }
      });
    });

    setErrors(newErrors);
    const newValid = Object.keys(newErrors).length === 0;
    setValid(newValid);

    return newValid;
  };

  return { validate, errors, valid };
}
