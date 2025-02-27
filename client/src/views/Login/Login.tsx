import { Login } from "@carbon/icons-react";
import { Button, Form, PasswordInput, ProgressBar, TextInput } from "@carbon/react";

import { ChangeEvent, useState } from "react";
import useValidation from "../../hooks/useValidation";
import authService from "../../services/auth";
import { required } from "../../utils/validators";
import './Login.scss';

interface LoginFormModel {
  login?: string
  password?: string
}

export default function LoginView() {
  const [model, setModel] = useState<LoginFormModel>({});
  const [processing, setProcessing] = useState<boolean>(false);

  const { validate, errors } = useValidation<LoginFormModel>({
    login: [required],
    password: [required]
  })

  const handleLoginChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, login: event.target.value })
  }

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, password: event.target.value })
  }

  const handleSignIn = async () => {
    if (validate(model)) {
      setProcessing(true);

      try {
        await authService.login<LoginFormModel>(model)
      } finally {
        setProcessing(false);
      }
    }
  }

  return <>
    { processing && <ProgressBar className="etlm-login--progress" label="" hideLabel /> }
    <div className="etlm-login">

      <Form>
        <TextInput id="login" labelText="Login" onChange={handleLoginChange} warn={!!errors?.login} warnText={errors?.login?.message} disabled={processing} />
        <PasswordInput id="password" labelText="Password" onChange={handlePasswordChange} warn={!!errors?.password} warnText={errors?.password?.message} disabled={processing} />
        <Button renderIcon={Login} onClick={handleSignIn} disabled={processing}>Sign In</Button>
      </Form>
    </div>
  </>
}
