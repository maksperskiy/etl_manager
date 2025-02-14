import { useState } from "react";

export interface ValidationError<T = unknown> {
  key: string
  value: T
  massage: string
}

export type Validator<T extends Record<string, unknown> = Record<string, unknown>> = (key: string, model: T) => true | ValidationError;

export interface ValidationSchema {
  [key: string]: Validator[]
}

export interface ValidationErrors {
  [key: string]: ValidationError
}

export default function useValidation<T extends Record<string, unknown> = Record<string, unknown>>(schema: ValidationSchema = {}) {
  const [valid, setValid] = useState<boolean>(true);
  const [errors, setErrors] = useState<ValidationErrors>({});

  const handler = (model: T) => {
    const newErrors: ValidationErrors = {};

    Object.entries(schema).forEach(([key, rules]) => {
      rules.find((rule: Validator) => {
        const validatorResult = rule(key, model);
        if (validatorResult !== true) {
          newErrors[key] = validatorResult;
          return true;
        }
      });
    });

    setErrors(newErrors);
    setValid(!Object.keys(newErrors).length);
  };

  return {
    valid,
    errors,
    handler
  }
}
