import { Route, Routes } from "react-router";
import Login from "./views/Login/Login";
import NotFound from "./views/NotFound/NotFound";

export default function Router() {
  return <Routes>
    <Route path="login" element={<Login />}></Route>
    <Route path="*" element={<NotFound />}></Route>
  </Routes>
}
