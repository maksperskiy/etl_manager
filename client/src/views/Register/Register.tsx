import { Button, Form, PasswordInput, ProgressBar, TextInput } from "@carbon/react";

import { Login } from "@carbon/icons-react";
import { ChangeEvent, useState } from "react";
import { Link } from "react-router";
import useValidation from "../../hooks/useValidation";
import commonService from "../../services/common";
import { email, required, Same } from "../../utils/validators";
import { LoginFormModel } from "../Login/Login";
import './Register.scss';

export interface RegisterFormModel extends Pick<LoginFormModel, 'username'> {
  password1?: string
  password2?: string
  email?: string
}

export default function RegisterView() {
  const [model, setModel] = useState<RegisterFormModel>({});
  const [processing, setProcessing] = useState<boolean>(false);

  const { validate, errors } = useValidation<RegisterFormModel>({
    username: [required],
    password1: [required],
    password2: [required, Same('password1', 'Passwords must be equal')],
    email: [required, email]
  })

  const handleUsernameChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, username: event.target.value })
  }

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, password1: event.target.value })
  }

  const handleRepeatPasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, password2: event.target.value })
  }

  const handleEmailChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, email: event.target.value })
  }

  const handleRegister = async () => {
    if (validate(model)) {
      setProcessing(true);

      try {
        await commonService.register(model)
      } finally {
        setProcessing(false);
      }
    }
  }

  return <>
    { processing && <ProgressBar className="etlm-register--progress" label="" hideLabel /> }
    <div className="etlm-register">
      <Form>
        <TextInput id="email" labelText="Email" onChange={handleEmailChange} warn={!!errors?.email} warnText={errors?.email?.message} disabled={processing} />
        <TextInput id="username" labelText="Username" onChange={handleUsernameChange} warn={!!errors?.login} warnText={errors?.login?.message} disabled={processing} />
        <PasswordInput id="password" labelText="Password" onChange={handlePasswordChange} warn={!!errors?.password1} warnText={errors?.password1?.message} disabled={processing} />
        <PasswordInput id="repeatPassword" labelText="Repeat Password" onChange={handleRepeatPasswordChange} warn={!!errors?.password2} warnText={errors?.password2?.message} disabled={processing} />
        <Button renderIcon={Login} onClick={handleRegister} disabled={processing}>Register</Button>
      </Form>
      <p>Already have an account? <Link to='/login'>Login here</Link></p>
    </div>
  </>
}
