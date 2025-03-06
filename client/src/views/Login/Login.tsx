import { Login } from "@carbon/icons-react";
import { Button, Form, PasswordInput, ProgressBar, TextInput } from "@carbon/react";

import { ChangeEvent, useState } from "react";
import { Link, useNavigate } from "react-router";
import useValidation from "../../hooks/useValidation";
import commonService from "../../services/common";
import useUserStore, { User } from "../../stores/user";
import { required } from "../../utils/validators";
import './Login.scss';

export interface LoginFormModel {
  username?: string
  password?: string
}

export default function LoginView() {
  const [model, setModel] = useState<LoginFormModel>({});
  const [processing, setProcessing] = useState<boolean>(false);

  const { setUser } = useUserStore(store => store);
  const navigate = useNavigate();

  const { validate, errors } = useValidation<LoginFormModel>({
    username: [required],
    password: [required]
  })

  const handleUsernameChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, username: event.target.value })
  }

  const handlePasswordChange = (event: ChangeEvent<HTMLInputElement>) => {
    setModel({ ...model, password: event.target.value })
  }

  const handleLogin = async () => {
    if (validate(model)) {
      setProcessing(true);

      try {
        const res = await commonService.login(model)
        setUser(((data: User) => ({ email: data.email, user_id: data.user_id, username: data.username }))(await res.json()))
        navigate('/')
      } finally {
        setProcessing(false);
      }
    }
  }

  return <>
    { processing && <ProgressBar className="etlm-login--progress" label="" hideLabel /> }
    <div className="etlm-login">
      <Form>
        <TextInput id="login" labelText="Username" onChange={handleUsernameChange} warn={!!errors?.login} warnText={errors?.login?.message} disabled={processing} />
        <PasswordInput id="password" labelText="Password" onChange={handlePasswordChange} warn={!!errors?.password} warnText={errors?.password?.message} disabled={processing} />
        <Button renderIcon={Login} onClick={handleLogin} disabled={processing}>Login</Button>
      </Form>
      <p>Have no account yet? <Link to='/register'>Register here</Link></p>
    </div>
  </>
}
